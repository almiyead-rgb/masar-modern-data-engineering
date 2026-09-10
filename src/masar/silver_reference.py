"""Independent, standard-library oracle for Lab 03, NOT a Lakehouse engine.

Source fixtures stay unchanged. Every returned row is an expected business
record used to test an eventual Spark/Delta readback, not a persisted Delta row.
"""
from __future__ import annotations
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo
from masar.workspace import require_fixed_dataset, rows_digest

TRIP_FIELDS = ('trip_id', 'driver_id', 'city', 'start_ts', 'end_ts', 'fare_sar', 'distance_km')
BUSINESS_FIELDS = ('trip_id', 'driver_id', 'city', 'start_utc', 'end_utc',
                   'trip_date_local', 'fare_sar', 'distance_km', 'duration_seconds',
                   'vehicle_type', 'driver_rating', 'source_revision')
CITIES = {'riyadh': 'Riyadh', 'jeddah': 'Jeddah', 'dammam': 'Dammam'}
TIME_RE = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(Z|[+-](0[0-9]|1[0-4]):[0-5][0-9])$"
NUMBER_RE = r"^[+-]?[0-9]+(\.[0-9]{1,2})?$"


def read_csv(source: Path, filename: str) -> list[dict]:
    if filename not in {'trips.csv', 'drivers.csv', 'late_trips.csv', 'quality_cases.csv', 'correction.csv'}:
        raise ValueError('Unsupported fixed source file')
    with (Path(source) / filename).open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    if any(None in row or any(v is None for v in row.values()) for row in rows):
        raise ValueError('Malformed CSV shape')
    return rows


def normalize_city(value: object) -> str | None:
    return CITIES.get(value.strip().lower()) if isinstance(value, str) else None


def parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not re.fullmatch(TIME_RE, value.strip()):
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace('Z', '+00:00'))
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        return None


def parse_measure(value: object, *, positive: bool = False) -> Decimal | None:
    if not isinstance(value, str) or not re.fullmatch(NUMBER_RE, value.strip()):
        return None
    try:
        number = Decimal(value.strip())
        if not number.is_finite() or number >= Decimal('10000000000'):
            return None
        if number < 0 or (positive and number == 0):
            return None
        return number.quantize(Decimal('0.01'))
    except InvalidOperation:
        return None


def drivers_index(rows: list[dict]) -> dict[str, dict]:
    result = {}
    for row in rows:
        key = row.get('driver_id', '').strip()
        vehicle = row.get('vehicle_type', '').strip().lower()
        rating_text = row.get('driver_rating', '').strip()
        try:
            rating = Decimal(rating_text)
        except InvalidOperation as exc:
            raise ValueError('Invalid driver rating') from exc
        if (not key or key in result or vehicle not in {'sedan', 'suv'}
                or not re.fullmatch(r'[0-9](\.[0-9])?', rating_text)
                or not rating.is_finite() or not 0 <= rating <= 5):
            raise ValueError('Driver dimension must have unique valid keys and attributes')
        result[key] = {'vehicle_type': vehicle, 'driver_rating': format(rating, '.1f')}
    if not result:
        raise ValueError('Empty driver dimension')
    return result


def normalize_trip(raw: dict, drivers: dict, revision: int = 1) -> tuple[dict | None, list[str]]:
    if type(revision) is not int or revision < 1:
        raise ValueError('Revision must be a positive integer')
    if any(field not in raw for field in TRIP_FIELDS):
        raise ValueError('Missing required trip columns')
    key = (raw.get('trip_id') or '').strip()
    driver = (raw.get('driver_id') or '').strip()
    city = normalize_city(raw.get('city'))
    start, end = parse_timestamp(raw.get('start_ts')), parse_timestamp(raw.get('end_ts'))
    fare = parse_measure(raw.get('fare_sar'))
    distance = parse_measure(raw.get('distance_km'), positive=True)
    reasons = []
    if not key: reasons.append('MISSING_TRIP_ID')
    if driver not in drivers: reasons.append('UNKNOWN_DRIVER')
    if city is None: reasons.append('INVALID_CITY')
    if start is None or end is None: reasons.append('INVALID_TIMESTAMP')
    elif end <= start: reasons.append('INVALID_DURATION')
    if fare is None: reasons.append('INVALID_FARE')
    if distance is None: reasons.append('INVALID_DISTANCE')
    if reasons:
        return None, reasons
    return dict(trip_id=key, driver_id=driver, city=city,
                start_utc=start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                end_utc=end.strftime('%Y-%m-%dT%H:%M:%SZ'),
                trip_date_local=start.astimezone(ZoneInfo('Asia/Riyadh')).date().isoformat(),
                fare_sar=format(fare, '.2f'), distance_km=format(distance, '.2f'),
                duration_seconds=int((end-start).total_seconds()),
                vehicle_type=drivers[driver]['vehicle_type'],
                driver_rating=drivers[driver]['driver_rating'], source_revision=revision), []


def conformed_rows(rows: list[dict], drivers: dict, revision: int = 1) -> tuple[list[dict], list[dict]]:
    accepted, rejected, unique = [], [], {}
    for position, row in enumerate(rows, 1):
        clean, reasons = normalize_trip(row, drivers, revision)
        if reasons:
            rejected.append({'source_row': position, 'trip_id': row.get('trip_id'), 'reasons': reasons})
        else:
            accepted.append(clean)
    for clean in accepted:
        key = clean['trip_id']
        if key in unique and unique[key] != clean:
            raise ValueError('Conflicting payloads at the same revision for trip ' + key)
        unique[key] = clean
    return sorted(unique.values(), key=lambda row: row['trip_id']), rejected


def merge_insert_only(existing: list[dict], incoming: list[dict]) -> list[dict]:
    """Pure expected-value calculation. No Delta MERGE executes here."""
    current = {}
    for row in existing:
        key = row['trip_id']
        if not key or key in current:
            raise ValueError('Target has missing or duplicate business keys')
        current[key] = dict(row)
    source_keys = [row['trip_id'] for row in incoming]
    if len(source_keys) != len(set(source_keys)) or any(not key for key in source_keys):
        raise ValueError('Incoming rows must be unique before the merge')
    for row in incoming:
        key = row['trip_id']
        if key in current and current[key] != row:
            raise ValueError('Insert-only Day 2 cannot silently apply a correction')
    for row in incoming:
        current.setdefault(row['trip_id'], dict(row))
    return sorted(current.values(), key=lambda row: row['trip_id'])


def reference_result(source: Path) -> dict:
    require_fixed_dataset(source)
    base = read_csv(source, 'trips.csv')
    late = read_csv(source, 'late_trips.csv')
    drivers = drivers_index(read_csv(source, 'drivers.csv'))
    initial, bad0 = conformed_rows(base + base, drivers)
    late_rows, bad1 = conformed_rows(late, drivers)
    rerun = merge_insert_only(initial, initial)
    final = merge_insert_only(initial, late_rows)
    repeated = merge_insert_only(final, late_rows)
    redelivered = merge_insert_only(repeated, initial + late_rows)
    fare0 = sum((Decimal(row['fare_sar']) for row in initial), Decimal('0'))
    fare1 = sum((Decimal(row['fare_sar']) for row in final), Decimal('0'))
    quality, bad = conformed_rows(read_csv(source, 'quality_cases.csv'), drivers)
    event_rows = [json.loads(s) for s in (Path(source)/'gps.ndjson').read_text().splitlines()]
    event_counts = Counter(e['trip_id'] for e in event_rows)
    raw_gps_join_count = sum(event_counts[row['trip_id']] for row in initial)
    before_date = Counter(row['trip_date_local'] for row in initial)
    after_date = Counter(row['trip_date_local'] for row in final)
    stages = [
        {'stage': 'base_and_replay', 'bronze_receipts': 144, 'silver_rows': len(initial), 'digest': rows_digest(initial)},
        {'stage': 'same_input_rerun', 'bronze_receipts': 144, 'silver_rows': len(rerun), 'digest': rows_digest(rerun)},
        {'stage': 'late_batch', 'bronze_receipts': 147, 'silver_rows': len(final), 'digest': rows_digest(final)},
        {'stage': 'same_batch_retry', 'bronze_receipts': 147, 'silver_rows': len(repeated), 'digest': rows_digest(repeated)},
        {'stage': 'intentional_redelivery', 'bronze_receipts': 150, 'silver_rows': len(redelivered), 'digest': rows_digest(redelivered)},
    ]
    checks = {
        'base_is_72': len(initial) == 72,
        'base_replay_same_content': initial == rerun,
        'late_adds_three': len(final) == 75,
        'late_replay_same_content': final == repeated == redelivered,
        'base_and_late_valid': not bad0 and not bad1,
        'all_driver_links_valid': all(row['driver_id'] in drivers for row in final),
        'one_row_per_trip': len({row['trip_id'] for row in final}) == len(final),
        'fare_reconciliation': fare1 - fare0 == Decimal('81.00'),
        'duration_positive': all(row['duration_seconds'] > 0 for row in final),
        'local_start_date_preserved': all(row['trip_date_local'] == '2026-06-01' for row in late_rows),
        'three_cities': set(row['city'] for row in final) == set(CITIES.values()),
        'driver_join_preserves_grain': len(initial) == 72,
        'raw_gps_join_multiplies_grain': raw_gps_join_count == 216,
        'three_gps_events_per_base_trip': set(event_counts.values()) == {3},
        'quality_fixture_rejected': not quality and len(bad) == 7,
        'seven_distinct_quality_reasons': len({r for row in bad for r in row['reasons']}) == 7,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {'scope': 'DAY02_REFERENCE_LOGIC_ONLY', 'engine_executed': False, 'dbt_executed': False,
            'dataset': 'MASAR_SMALL_V1', 'stages': stages, 'checks': checks,
            'base_fare_sar': format(fare0, '.2f'), 'final_fare_sar': format(fare1, '.2f'),
            'late_added_fare_sar': format(fare1-fare0, '.2f'),
            'dates_before': dict(sorted(before_date.items())), 'dates_after': dict(sorted(after_date.items())),
            'base_city_normalizations': sum(row['city'] != normalize_city(row['city']) for row in base),
            'join_demo': {'trip_rows':72, 'raw_gps_join_rows':raw_gps_join_count,
                          'note':'Raw one-to-many GPS joins change the grain; aggregate events before a trip-grain join.'},
            'quality_examples': bad, 'expected_silver_rows': final}
