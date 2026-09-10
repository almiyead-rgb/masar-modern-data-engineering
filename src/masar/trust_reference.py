"""Day 4 source-derived expectations and explicit quality policy.

No Kafka offsets, checkpoint files, Delta commits or GX reports are simulated.
The same rule policy is reusable after a real Delta read; engine proof remains
separate. All outputs are deterministic and source files are read-only.
"""
from __future__ import annotations
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo
from masar.delta_reference import day03_reference
from masar.silver_reference import (
    BUSINESS_FIELDS, CITIES, TRIP_FIELDS, drivers_index, normalize_city,
    parse_timestamp, read_csv,
)
from masar.workspace import DATASET_MANIFEST_SHA256, require_fixed_dataset, rows_digest

GPS_FILES = ('gps.ndjson', 'gps_replay.ndjson', 'gps_late.ndjson')
SCENARIO_AS_OF = '2026-06-04T03:04:00Z'
SCENARIO_DELIVERY = '2026-06-04T03:00:00Z'
QUALITY_RULE_VERSION = 'MASAR_QUALITY_V1'


def events_from_source(source: Path, filename: str) -> list[dict]:
    if filename not in GPS_FILES:
        raise ValueError('Use a fixed GPS fixture')
    require_fixed_dataset(source)
    events = [json.loads(line) for line in (Path(source) / filename).read_text(encoding='utf-8').splitlines()]
    return events


def event_contract(event: dict, trip_ids: set[str]) -> list[str]:
    reasons = []
    fields = {'event_id', 'trip_id', 'event_ts', 'city', 'location', 'synthetic'}
    if not isinstance(event, dict) or set(event) != fields:
        return ['EVENT_SCHEMA_MISMATCH']
    if not isinstance(event['event_id'], str) or not event['event_id'].strip():
        reasons.append('MISSING_EVENT_ID')
    if not isinstance(event['trip_id'], str) or event['trip_id'] not in trip_ids:
        reasons.append('UNKNOWN_TRIP')
    if parse_timestamp(event['event_ts']) is None:
        reasons.append('INVALID_EVENT_TIME')
    if event['city'] not in CITIES.values():
        reasons.append('INVALID_CITY')
    if event['synthetic'] is not True:
        reasons.append('NON_SYNTHETIC_EVENT')
    loc = event['location']
    if not isinstance(loc, dict) or set(loc) != {'lat', 'lon'}:
        reasons.append('INVALID_LOCATION')
    else:
        for name, lower, upper in [('lat', -90, 90), ('lon', -180, 180)]:
            value = loc[name]
            if type(value) not in (int, float) or not math.isfinite(value) or not lower <= value <= upper:
                reasons.append('INVALID_' + name.upper())
    return reasons


def unique_events(events: list[dict]) -> list[dict]:
    """Drop identical deliveries only; conflicting payloads must never be hidden."""
    index = {}
    for event in events:
        key = event.get('event_id')
        if not isinstance(key, str) or not key.strip():
            raise ValueError('Event key is required')
        if key in index and index[key] != event:
            raise ValueError('Conflicting event payload for ' + key)
        index[key] = deepcopy(event)
    return [index[key] for key in sorted(index)]


def decimal_value(value: object) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        parsed = Decimal(str(value))
        return parsed if parsed.is_finite() else None
    except (ValueError, InvalidOperation):
        return None


def quality_probe_rows(source: Path) -> list[dict]:
    """Project deliberately bad raw rows into the business schema without fixing them.

    This is a reference projection, not native Spark type enforcement. Invalid
    parse results stay null; negative and zero values remain available to test.
    Native Lab 06 uses Spark's actual projection and compares the root reasons.
    """
    drivers = drivers_index(read_csv(source, 'drivers.csv'))
    projected = []
    for raw in read_csv(source, 'quality_cases.csv'):
        start, end = parse_timestamp(raw['start_ts']), parse_timestamp(raw['end_ts'])
        driver = raw['driver_id'].strip()
        attrs = drivers.get(driver, {})
        def number(name):
            n = decimal_value(raw[name])
            return format(n, '.2f') if n is not None else None
        projected.append(dict(
            trip_id=raw['trip_id'].strip(), driver_id=driver, city=normalize_city(raw['city']),
            start_utc=start.strftime('%Y-%m-%dT%H:%M:%SZ') if start else None,
            end_utc=end.strftime('%Y-%m-%dT%H:%M:%SZ') if end else None,
            trip_date_local=start.astimezone(ZoneInfo('Asia/Riyadh')).date().isoformat() if start else None,
            fare_sar=number('fare_sar'), distance_km=number('distance_km'),
            duration_seconds=int((end-start).total_seconds()) if start and end else None,
            vehicle_type=attrs.get('vehicle_type'), driver_rating=attrs.get('driver_rating'),
            source_revision=1))
    return projected


def row_quality_reasons(row: dict, driver_ids: set[str]) -> list[str]:
    if set(row) != set(BUSINESS_FIELDS):
        return ['BUSINESS_SCHEMA_MISMATCH']
    reasons = []
    key = row['trip_id']
    if not isinstance(key, str) or not key.strip() or key != key.strip():
        reasons.append('MISSING_TRIP_ID')
    driver = row['driver_id']
    if not isinstance(driver, str) or driver not in driver_ids:
        reasons.append('UNKNOWN_DRIVER')
    if row['city'] not in CITIES.values():
        reasons.append('INVALID_CITY')
    start, end = parse_timestamp(row['start_utc']), parse_timestamp(row['end_utc'])
    if start is None or end is None:
        reasons.append('INVALID_TIMESTAMP')
    else:
        duration = int((end-start).total_seconds())
        if (duration <= 0 or type(row['duration_seconds']) is not int
                or row['duration_seconds'] != duration):
            reasons.append('INVALID_DURATION')
        expected_date = start.astimezone(ZoneInfo('Asia/Riyadh')).date().isoformat()
        if row['trip_date_local'] != expected_date:
            reasons.append('INVALID_LOCAL_DATE')
    fare, distance, rating = [decimal_value(row[k]) for k in ('fare_sar','distance_km','driver_rating')]
    if fare is None or not Decimal(0) <= fare < Decimal('10000000000'):
        reasons.append('INVALID_FARE')
    if distance is None or not Decimal(0) < distance < Decimal('10000000000'):
        reasons.append('INVALID_DISTANCE')
    if isinstance(driver, str) and driver in driver_ids and (row['vehicle_type'] not in {'sedan','suv'} or rating is None or not 0 <= rating <= 5):
        reasons.append('INVALID_DRIVER_ATTRIBUTES')
    if type(row['source_revision']) is not int or row['source_revision'] < 1:
        reasons.append('INVALID_REVISION')
    return reasons


def evaluate_quality(rows: list[dict], driver_ids: set[str], *, expected_rows: int = 75) -> dict:
    """Strict whole-batch gate: quarantine invalid rows, but do not publish a subset.

    The clean subset can be revalidated as a new candidate. Every duplicate key
    is isolated, including its first occurrence; this is not a deduplication step.
    Counts are classroom fixture contracts, never production SLOs.
    """
    if type(expected_rows) is not int or expected_rows <= 0 or not driver_ids:
        raise ValueError('A positive fixture count and a non-empty driver dimension are required')
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError('Quality input must contain dictionaries')
    keys = Counter(r.get('trip_id') for r in rows if isinstance(r.get('trip_id'), str) and r['trip_id'].strip())
    accepted, quarantine = [], []
    for position, row in enumerate(rows, 1):
        reasons = row_quality_reasons(row, driver_ids)
        if isinstance(row.get('trip_id'), str) and keys.get(row['trip_id'], 0) > 1:
            reasons.append('DUPLICATE_TRIP_ID')
        if reasons:
            quarantine.append({'candidate_row': position, 'trip_id': row.get('trip_id'),
                               'reason_codes': reasons, 'row': deepcopy(row)})
        else:
            accepted.append(deepcopy(row))
    blockers = []
    if len(rows) != expected_rows: blockers.append('VOLUME_MISMATCH')
    if any('BUSINESS_SCHEMA_MISMATCH' in x['reason_codes'] for x in quarantine): blockers.append('SCHEMA_MISMATCH')
    if quarantine: blockers.append('ROW_RULE_FAILURE')
    return {'scope': 'QUALITY_POLICY_EVALUATION_NOT_GX', 'gx_executed': False,
        'rule_version': QUALITY_RULE_VERSION, 'input_rows': len(rows), 'expected_rows': expected_rows,
        'accepted_rows': len(accepted), 'rejected_rows': len(quarantine),
        'rejection_rate': len(quarantine) / len(rows) if rows else None,
        'batch_blockers': blockers, 'promote_allowed': not blockers,
        'accepted': accepted, 'quarantine': quarantine,
        'reason_counts': dict(sorted(Counter(code for r in quarantine for code in r['reason_codes']).items()))}


def freshness(observed: str, as_of: str, *, max_age_seconds: int) -> dict:
    if type(max_age_seconds) is not int or max_age_seconds < 0:
        raise ValueError('Freshness threshold must be a non-negative integer')
    timestamp, now = parse_timestamp(observed), parse_timestamp(as_of)
    if timestamp is None or now is None:
        raise ValueError('Use explicit timezone-aware timestamps')
    age = int((now-timestamp).total_seconds())
    return {'age_seconds': age, 'limit_seconds': max_age_seconds,
            'status': 'FUTURE_TIMESTAMP' if age < 0 else ('PASS' if age <= max_age_seconds else 'STALE')}


def city_distribution(rows: list[dict], baseline: list[dict], *, threshold: float = 0.10) -> dict:
    """Categorical total-variation distance; a warning, not a hypothesis test."""
    if not rows or not baseline or not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError('Need non-empty cohorts and threshold in [0,1]')
    a, b = Counter(r['city'] for r in rows), Counter(r['city'] for r in baseline)
    keys = sorted(set(a) | set(b))
    distance = 0.5 * sum(abs(a[k]/len(rows) - b[k]/len(baseline)) for k in keys)
    return {'metric': 'categorical_total_variation_distance', 'value': distance,
            'threshold': threshold, 'status': 'WARN' if distance > threshold else 'PASS',
            'current_counts': dict(a), 'baseline_counts': dict(b),
            'meaning': 'Fixture-relative diagnostic; not statistical significance or real population drift.'}


def day04_reference(source: Path) -> dict:
    require_fixed_dataset(source)
    previous = day03_reference(source)
    trips = previous['expected_corrected_rows']
    drivers = set(drivers_index(read_csv(source, 'drivers.csv')))
    trip_ids = {r['trip_id'] for r in trips}
    base, replay, late = [events_from_source(source, name) for name in GPS_FILES]
    all_events = base + replay + late
    event_issues = [event_contract(e, trip_ids) for e in all_events]
    unique = unique_events(all_events)
    clean = evaluate_quality(trips, drivers)
    mixed = evaluate_quality(trips + quality_probe_rows(source), drivers)
    rechecked = evaluate_quality(mixed['accepted'], drivers)
    newest = max(parse_timestamp(e['event_ts']) for e in all_events).strftime('%Y-%m-%dT%H:%M:%SZ')
    oldest = min(parse_timestamp(e['event_ts']) for e in all_events).strftime('%Y-%m-%dT%H:%M:%SZ')
    checks = {
        'all_event_contracts_valid': not any(event_issues),
        'base_source_has_216_events': len(base) == len(unique_events(base)) == 216,
        'replay_two_already_known_events': len(replay) == 2 and len(unique_events(base+replay)) == 216,
        'late_adds_one_new_event': len(late) == 1 and len(unique) == 217,
        'total_deliveries_219_not_219_unique_events': len(all_events) == 219 and len(unique) == 217,
        'late_event_time_is_older_than_last_base_event': parse_timestamp(late[0]['event_ts']) < max(parse_timestamp(e['event_ts']) for e in base),
        'every_event_links_to_known_trip': all(e['trip_id'] in trip_ids for e in unique),
        'clean_75_passes_policy': clean['promote_allowed'] and clean['accepted_rows'] == 75,
        'mixed_82_fails_and_quarantines_7': not mixed['promote_allowed'] and mixed['input_rows'] == 82 and mixed['rejected_rows'] == 7,
        'seven_root_reasons_are_retained': len(mixed['reason_counts']) == 7,
        'clean_recheck_matches_trusted_silver': rechecked['promote_allowed'] and rechecked['accepted'] == trips,
        'corrected_fare_total_preserved': sum(Decimal(r['fare_sar']) for r in rechecked['accepted']) == Decimal('1880.60'),
        'source_hashes_unchanged': bool(require_fixed_dataset(source)),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {'scope':'DAY04_SOURCE_EXPECTATIONS_ONLY', 'engine_executed':False,
        'kafka_executed':False, 'gx_executed':False,
        'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,
        'deliveries': {'base':len(base),'replay':len(replay),'late':len(late),'total':len(all_events)},
        'distinct_events':len(unique), 'identical_repeated_deliveries':len(all_events)-len(unique),
        'unique_events_digest':rows_digest(unique),
        'trusted_rows':len(trips),'trusted_fare_sar':'1880.60',
        'trusted_business_digest':rows_digest(trips),
        'quality_clean': {k:v for k,v in clean.items() if k not in {'accepted','quarantine'}},
        'quality_mixed':{k:v for k,v in mixed.items() if k != 'accepted'},
        'scenario_clock':SCENARIO_AS_OF,
        'event_time_newest':newest,'event_time_oldest':oldest,
        'source_event_freshness':freshness(newest,SCENARIO_AS_OF,max_age_seconds=12*3600),
        'delivery_freshness':freshness(SCENARIO_DELIVERY,SCENARIO_AS_OF,max_age_seconds=5*60),
        'city_distribution_vs_day03':city_distribution(rechecked['accepted'],trips),
        'checks':checks,
        'not_proven':['Kafka delivery','checkpoint recovery','watermark behaviour','Spark/Delta execution',
                      'Great Expectations validation','GX Data Docs','access control enforcement']}
