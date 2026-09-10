"""Validate the shape of native evidence, never simulate engine execution.

Checksums bind locally produced reports to files. They are not signatures or
proof against a person who controls and rewrites the complete evidence bundle.
"""
from __future__ import annotations
import json
from pathlib import Path
from masar.workspace import DATASET_MANIFEST_SHA256, workspace_path, digest_file

# Logical stages, not additional student labs: 3a/3b and 4a/4b share their lab.
STAGES = {
    'lab01_bronze': ('reports/bronze.json', 'DAY01_BRONZE_ENGINE', {
        'expected_totals', 'two_trip_deliveries', 'business_trip_count_unchanged',
        'initial_snapshot_retained', 'base_csv_columns_are_strings',
        'payloads_and_source_hashes_preserved', 'real_delta_files_present'}),
    'lab02_scan': ('reports/benchmark.json', 'DAY01_SPARK_LOCAL_BENCHMARK', {
        'equal_source_populations', 'query_results_match_oracle', 'positive_measured_samples', 'query_plans_saved'}),
    'lab03a_staging': ('reports/day02_staging_latest.json', 'DAY02_STAGING_ENGINE', {
        'counts_verified', 'typed_values_match_source_oracle', 'drivers_unique_and_join_safe', 'gps_valid', 'delta_readback'}),
    'lab03b_silver': ('reports/day02_silver.json', 'DAY02_SILVER_ENGINE', {
        'all_scenarios_match_independent_oracle', 'business_keys_unique',
        'replay_preserves_business_content', 'late_rows_retained', 'actual_delta_files'}),
    'lab04a_transactions': ('reports/day03_transactions.json', 'DAY03_TRANSACTIONS_ENGINE', {
        'native_correction_matches_source_expectation', 'business_rows_stay_75',
        'replay_and_stale_delivery_preserve_values', 'same_revision_conflict_rejected',
        'actual_prior_version_read', 'mixed_valid_invalid_batch_rejected_atomically'}),
    'lab04b_maintenance': ('reports/day03_maintenance_latest.json', 'DAY03_MAINTENANCE_ENGINE', {
        'unexpected_column_rejected', 'approved_evolution_preserves_business_values',
        'compaction_preserves_values', 'delete_affects_copy_only', 'restore_creates_new_commit',
        'vacuum_is_non_destructive_dry_run', 'trusted_silver_unchanged'}),
    'lab05_streaming': ('reports/day04_stream_latest.json', 'DAY04_NATIVE_STREAMING', {
        'phase_transport_counts', 'phase_event_counts', 'transport_keys_always_unique',
        'restart_same_query_identity', 'restart_new_execution_ids', 'checkpoint_same_for_all_phases',
        'actual_checkpoint_files_present', 'producer_consumer_offsets_reconcile',
        'source_json_text_preserved', 'event_content_matches_source', 'unique_events_delta_readback',
        'all_events_link_to_trusted_trips', 'late_event_retained'}),
    'lab06_quality': ('reports/day04_quality_latest.json', 'DAY04_NATIVE_QUALITY', {
        'trusted_and_rechecked_pass_gx', 'mixed_candidate_fails_gx', 'native_mixed_counts',
        'native_reasons_match_reference', 'failed_candidate_not_promoted', 'quarantine_delta_readback',
        'approved_readback_same_business_contents', 'source_silver_untouched', 'data_docs_exist_for_all_three_cases'}),
    'lab07_gold_recovery': ('reports/day05_recovery.json', 'DAY05_NATIVE_RECOVERY', {
        'injected_failure_observed', 'previous_release_preserved', 'rebuild_has_new_identity', 'content_equal'}),
    'lab08_serving': ('reports/day05_serving_latest.json', 'DAY05_NATIVE_SERVING', {
        'fact_grain_75', 'foreign_keys_valid', 'gold_fact_totals_match', 'events_aggregated_before_join',
        'group_grains_reconcile', 'labels_not_fabricated', 'feature_availability_checked', 'feature_label_keys_aligned'}),
}


def validate_stage_result(name: str, report: dict) -> None:
    """Reject failed, empty, wrong-scope or helper results before the next stage."""
    if not isinstance(report, dict) or report.get('engine_executed') is not True:
        raise ValueError('Native execution evidence is missing: ' + name)
    if not isinstance(report.get('scope'), str) or not report['scope'].strip():
        raise ValueError('Named evidence scope is missing: ' + name)
    if 'status' in report and report['status'] not in {'PASSED', 'SUCCEEDED'}:
        raise ValueError('Native stage reports a non-success status: ' + name)
    if report.get('complete_lab_success') is False or report.get('success') is False:
        raise ValueError('Native stage explicitly failed: ' + name)
    checks = report.get('checks')
    if (not isinstance(checks, dict) or not checks or
            not all(isinstance(k, str) and k and v is True for k, v in checks.items())):
        raise ValueError('Native stage checks are missing, empty or failed: ' + name)
    if name in STAGES:
        _, scope, required = STAGES[name]
        if report['scope'] != scope or not required.issubset(checks):
            raise ValueError('Wrong scope or incomplete required checks: ' + name)
        if report.get('dataset_manifest_sha256') != DATASET_MANIFEST_SHA256:
            raise ValueError('Native report refers to another dataset: ' + name)
        for stage, flag in [('lab05_streaming', 'kafka_executed'), ('lab06_quality', 'gx_executed')]:
            if name == stage and report.get(flag) is not True:
                raise ValueError('Required component did not execute: ' + flag)


def verify_artifact_records(work: Path, value) -> int:
    """Check every nested path/SHA256 pair against non-empty, non-symlink files."""
    total = 0
    if isinstance(value, dict):
        if 'path' in value and 'sha256' in value:
            path = workspace_path(work, value['path'])
            if (not path.is_file() or path.stat().st_size == 0 or
                    digest_file(path) != value['sha256']):
                raise ValueError('Missing or changed native artifact: ' + str(value['path']))
            total += 1
        for nested in value.values():
            total += verify_artifact_records(work, nested)
    elif isinstance(value, list):
        total += sum(verify_artifact_records(work, v) for v in value)
    return total


def read_stage_report(work: Path, name: str) -> dict:
    path, _, _ = STAGES[name]
    report = json.loads(workspace_path(work, path).read_text(encoding='utf-8'))
    validate_stage_result(name, report)
    # Benchmark and recovery are supported by their plans/release, not invented Delta paths.
    if name not in {'lab02_scan', 'lab07_gold_recovery', 'lab08_serving'}:
        if verify_artifact_records(work, report.get('artifacts')) < 2:
            raise ValueError('Actual Delta log and data artifacts are missing: ' + name)
    if name == 'lab02_scan':
        from masar.workspace import summarize_samples
        if report.get('population_rows') != 72 or report.get('snapshot_version') != 0:
            raise ValueError('Benchmark populations changed')
        measurements = report.get('measurements', {})
        if set(measurements) != {'csv', 'delta_v0'}:
            raise ValueError('Both benchmark variants are required')
        for variant in measurements:
            summarize_samples(measurements[variant]['samples_s'])
            plan = workspace_path(work, report['plans'][variant])
            if not plan.is_file() or not plan.read_text(encoding='utf-8').strip():
                raise ValueError('Measured query plan is missing')
    return report
