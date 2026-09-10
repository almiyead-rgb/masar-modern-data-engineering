"""Day 3 expected business values, not an implementation or simulation of Delta.

This module does not create table versions, transaction logs, or fake engine
results. It calculates source-derived values used to check real lab outputs.
"""
from __future__ import annotations
import csv
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from masar.silver_reference import (
    BUSINESS_FIELDS, TRIP_FIELDS, conformed_rows, drivers_index,
    normalize_trip, parse_measure, read_csv, reference_result,
)
from masar.workspace import DATASET_MANIFEST_SHA256, require_fixed_dataset, rows_digest


def _index(rows: list[dict], label: str) -> dict[str, dict]:
    result = {}
    for row in rows:
        if set(row) != set(BUSINESS_FIELDS):
            raise ValueError(label + ': use the documented business fields only')
        key = row['trip_id']
        revision = row['source_revision']
        if not isinstance(key, str) or not key.strip() or key != key.strip() or key in result:
            raise ValueError(label + ': missing, untrimmed or duplicate trip key')
        if type(revision) is not int or revision < 1:
            raise ValueError(label + ': revision must be a positive integer')
        result[key] = deepcopy(row)
    return result


def revision_merge(existing: list[dict], incoming: list[dict]) -> tuple[list[dict], list[dict]]:
    """Calculate expected values with explicit revision ordering; never mutate inputs.

    Same-key/same-revision disagreements fail before any result is returned.
    A lower revision is ignored even when it arrives later. Keys must already
    be unique and payloads must have passed the Day 2 normalization contract.
    """
    target, source = _index(existing, 'target'), _index(incoming, 'source')
    for key, row in source.items():
        if key in target and row['source_revision'] == target[key]['source_revision'] and row != target[key]:
            raise ValueError('Same-revision conflict for ' + key)
    actions = []
    for key in sorted(source):
        row = source[key]
        if key not in target:
            action = 'INSERT'
            target[key] = deepcopy(row)
        elif row['source_revision'] > target[key]['source_revision']:
            action = 'UPDATE_NEWER_REVISION'
            target[key] = deepcopy(row)
        elif row['source_revision'] < target[key]['source_revision']:
            action = 'IGNORE_STALE_REVISION'
        else:
            action = 'IDENTICAL_REPLAY'
        actions.append({'trip_id': key, 'action': action})
    return [target[key] for key in sorted(target)], actions


def schema_fixture(source: Path) -> dict:
    require_fixed_dataset(source)
    with (Path(source) / 'schema_change.csv').open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    if fields != list(TRIP_FIELDS) + ['surcharge_sar'] or len(rows) != 1:
        raise ValueError('Unexpected schema-change fixture')
    row = rows[0]
    amount = parse_measure(row['surcharge_sar'])
    if amount is None:
        raise ValueError('The approved extra field must be a non-negative decimal')
    drivers = drivers_index(read_csv(source, 'drivers.csv'))
    normalized, reasons = normalize_trip({name: row[name] for name in TRIP_FIELDS}, drivers)
    if reasons:
        raise ValueError('Schema fixture contains invalid base fields')
    return {'extra_column': 'surcharge_sar', 'spark_type': 'decimal(12,2)',
            'trip_id': normalized['trip_id'], 'value': format(amount, '.2f'),
            'business_row': normalized,
            'meaning': 'Separate surcharge; do not silently redefine fare_sar.'}


def day03_reference(source: Path) -> dict:
    require_fixed_dataset(source)
    day02 = reference_result(source)
    before = day02['expected_silver_rows']
    drivers = drivers_index(read_csv(source, 'drivers.csv'))
    correction, rejected = conformed_rows(read_csv(source, 'correction.csv'), drivers, revision=2)
    if rejected or len(correction) != 1 or correction[0]['trip_id'] != 'SYN_T0001':
        raise AssertionError('Unexpected correction fixture')
    after, actions = revision_merge(before, correction)
    replay, _ = revision_merge(after, correction)
    stale, stale_actions = revision_merge(after, before)
    conflict = deepcopy(correction)
    conflict[0]['fare_sar'] = '24.00'  # transient negative-test probe; no source file is changed
    conflict_rejected = False
    try:
        revision_merge(after, conflict)
    except ValueError as exc:
        if 'Same-revision conflict' not in str(exc):
            raise
        conflict_rejected = True
    before_trip = next(row for row in before if row['trip_id'] == 'SYN_T0001')
    after_trip = next(row for row in after if row['trip_id'] == 'SYN_T0001')
    total_before = sum((Decimal(row['fare_sar']) for row in before), Decimal(0))
    total_after = sum((Decimal(row['fare_sar']) for row in after), Decimal(0))
    changed = [old['trip_id'] for old, new in zip(before, after) if old != new]
    fixture = schema_fixture(source)
    quality = reference_result(source)['quality_examples']
    checks = {
        'input_has_75_unique_trips': len(before) == len({r['trip_id'] for r in before}) == 75,
        'correction_targets_existing_trip': correction[0]['trip_id'] in {r['trip_id'] for r in before},
        'correction_changes_one_trip': changed == ['SYN_T0001'],
        'fare_changes_18_to_23': (before_trip['fare_sar'], after_trip['fare_sar']) == ('18.00', '23.00'),
        'revision_changes_1_to_2': (before_trip['source_revision'], after_trip['source_revision']) == (1, 2),
        'row_count_stays_75': len(after) == 75,
        'fare_total_increases_by_5': total_after - total_before == Decimal('5.00'),
        'replay_preserves_business_values': replay == after,
        'stale_redelivery_does_not_undo_correction': stale == after,
        'same_revision_conflict_rejected': conflict_rejected,
        'only_one_source_revision_is_2': sum(r['source_revision'] == 2 for r in after) == 1,
        'schema_fixture_is_one_extra_field': fixture['extra_column'] == 'surcharge_sar',
        'surcharge_fixture_2_not_part_of_fare': fixture['value'] == '2.00',
        'seven_quality_probes_remain_invalid': len(quality) == 7,
        'source_manifest_unchanged': bool(require_fixed_dataset(source)),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {
        'scope': 'DAY03_REFERENCE_BUSINESS_VALUES_ONLY', 'engine_executed': False,
        'dataset': 'MASAR_SMALL_V1', 'dataset_manifest_sha256': DATASET_MANIFEST_SHA256,
        'correction_revision_source': 'Lab scenario metadata; revision is not a field in correction.csv',
        'before': {'rows': len(before), 'fare_sar': format(total_before, '.2f'), 'digest': rows_digest(before)},
        'after': {'rows': len(after), 'fare_sar': format(total_after, '.2f'), 'digest': rows_digest(after)},
        'corrected_trip_before': before_trip, 'corrected_trip_after': after_trip,
        'replay_digest': rows_digest(replay), 'stale_replay_digest': rows_digest(stale),
        'correction_actions': actions,
        'stale_ignored_count': sum(a['action'] == 'IGNORE_STALE_REVISION' for a in stale_actions),
        'schema_fixture': fixture, 'quality_examples': quality,
        'checks': checks, 'expected_corrected_rows': after,
        'not_proven': ['Delta transactions', 'ACID engine behaviour', 'time travel',
                       'schema enforcement', 'OPTIMIZE', 'RESTORE', 'VACUUM', 'concurrency'],
    }
