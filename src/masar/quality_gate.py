"""Native Lab 06: real Delta snapshots, real GX Checkpoints and local Data Docs.

The quality policy adds row-level quarantine and explicit promotion decisions;
GX does not move or fix rows automatically. Source Silver is never overwritten.
"""
from __future__ import annotations
import importlib.metadata
import json
from pathlib import Path
import uuid
from masar.runtime import EnvironmentUnavailable
from masar.workspace import (workspace_path,write_json,require_fixed_dataset,rows_digest,
                             DATASET_MANIFEST_SHA256,digest_file)
from masar.silver_reference import BUSINESS_FIELDS,drivers_index,read_csv
from masar.delta_reference import day03_reference
from masar.trust_reference import (evaluate_quality,day04_reference,city_distribution,
                                  QUALITY_RULE_VERSION)
GX_VERSION='1.7.0'
PANDAS_VERSION='2.2.3'


def quality_preflight() -> dict:
    packages={};issues=[]
    for name,version in [('great-expectations',GX_VERSION),('pandas',PANDAS_VERSION)]:
        try: observed=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: observed=None
        packages[name]={'required':version,'observed':observed}
        if observed!=version: issues.append(f'{name}: required {version}, observed {observed}')
    return {'scope':'QUALITY_DEPENDENCY_CHECK_ONLY','gx_executed':False,'packages':packages,'issues':issues}


def completed_day03_table(spark,source:Path,work:Path):
    from masar.silver import canonical_rows,delta_artifacts
    require_fixed_dataset(source)
    if spark.conf.get('spark.sql.session.timeZone')!='UTC': raise ValueError('UTC Spark session required')
    report=json.loads(workspace_path(work,'reports/day03_transactions.json').read_text(encoding='utf-8'))
    if (report.get('scope')!='DAY03_TRANSACTIONS_ENGINE' or report.get('engine_executed') is not True
        or report.get('dataset_manifest_sha256')!=DATASET_MANIFEST_SHA256
        or not report.get('checks') or not all(v is True for v in report['checks'].values())):
        raise ValueError('Verified cumulative Day 3 Silver is required')
    path=workspace_path(work,'mini_lakehouse/silver/trips')
    frame=spark.read.format('delta').load(str(path))
    if frame.limit(501).count()>500: raise ValueError('This bounded teaching lab is limited to 500 trips')
    if canonical_rows(frame)!=day03_reference(source)['expected_corrected_rows']:
        raise ValueError('Actual Silver does not match the approved corrected dataset')
    delta_artifacts(work,path)
    return frame


def gx_validate_rows(rows:list[dict],driver_ids:set[str],context_root:Path,phase:str) -> dict:
    """Real GX 1.x DataFrame validation. Only an executed Checkpoint can return success.

    The bounded Pandas frame is collected from a real Delta snapshot by the native
    wrapper. This is an explicit teaching choice, not distributed validation.
    """
    report=quality_preflight()
    if report['issues']: raise EnvironmentUnavailable('; '.join(report['issues']))
    if phase not in {'trusted','mixed','rechecked'}: raise ValueError('Unknown GX phase')
    if not 1<=len(rows)<=500: raise ValueError('Use a bounded non-empty snapshot, at most 500 rows')
    if context_root.exists(): raise ValueError('Use a fresh context directory; preserve previous Data Docs')
    import pandas as pd
    import great_expectations as gx
    import great_expectations.expectations as gxe
    frame=pd.DataFrame(rows,columns=list(BUSINESS_FIELDS))
    for name in ('fare_sar','distance_km','driver_rating','source_revision','duration_seconds'):
        frame[name]=pd.to_numeric(frame[name],errors='coerce')
    # Canonical ISO UTC strings are fixed-width: lexicographic ordering agrees
    # with time ordering; the policy also validates actual datetime parsing.
    context_root.mkdir(parents=True)
    context=gx.get_context(mode='file',project_root_dir=str(context_root))
    data_source=context.data_sources.add_pandas(name='masar_silver')
    asset=data_source.add_dataframe_asset(name='silver_trips_snapshot')
    batch=asset.add_batch_definition_whole_dataframe('whole_snapshot')
    suite=gx.ExpectationSuite(name='masar_silver_quality_v1')
    suite.add_expectation(gxe.ExpectTableColumnsToMatchOrderedList(column_list=list(BUSINESS_FIELDS)))
    suite.add_expectation(gxe.ExpectTableRowCountToEqual(value=75))
    for name in BUSINESS_FIELDS:
        suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column=name))
    suite.add_expectation(gxe.ExpectColumnValuesToBeUnique(column='trip_id'))
    suite.add_expectation(gxe.ExpectColumnValuesToMatchRegex(column='trip_id',regex=r'^SYN_[A-Z0-9]+$'))
    suite.add_expectation(gxe.ExpectColumnValuesToBeInSet(column='driver_id',value_set=sorted(driver_ids)))
    suite.add_expectation(gxe.ExpectColumnValuesToBeInSet(column='city',value_set=['Riyadh','Jeddah','Dammam']))
    suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column='fare_sar',min_value=0,max_value=1e10,strict_max=True))
    suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column='distance_km',min_value=0,strict_min=True,max_value=1e10,strict_max=True))
    suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column='duration_seconds',min_value=0,strict_min=True))
    suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column='source_revision',min_value=1))
    suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column='driver_rating',min_value=0,max_value=5))
    suite.add_expectation(gxe.ExpectColumnValuesToBeInSet(column='vehicle_type',value_set=['sedan','suv']))
    suite.add_expectation(gxe.ExpectColumnPairValuesAToBeGreaterThanB(
        column_A='end_utc',column_B='start_utc',or_equal=False,ignore_row_if='either_value_is_missing'))
    suite=context.suites.add(suite)
    definition=context.validation_definitions.add(gx.ValidationDefinition(
        name='validate_'+phase,data=batch,suite=suite))
    checkpoint=context.checkpoints.add(gx.Checkpoint(name='checkpoint_'+phase,
        validation_definitions=[definition],
        actions=[gx.checkpoint.UpdateDataDocsAction(name='build_local_data_docs')],
        result_format={'result_format':'SUMMARY'}))
    result=checkpoint.run(batch_parameters={'dataframe':frame})
    payload={'success':bool(result.success), 'phase':phase,
        'run_results':{str(key):{'success':bool(value.success),
            'statistics':value.statistics} for key,value in result.run_results.items()}}
    write_json(context_root/'checkpoint_result.json',payload)
    context.build_data_docs()
    html=sorted(context_root.rglob('index.html'))
    if not html or not any(p.stat().st_size>0 for p in html):
        raise AssertionError('GX validation ran but local Data Docs were not generated')
    return {'scope':'GX_NATIVE_CHECKPOINT','gx_executed':True,'gx_version':gx.__version__,
            'phase':phase,'success':bool(result.success),'rows':len(rows),
            'checkpoint_result_file':'checkpoint_result.json',
            'data_docs':[p.relative_to(context_root).as_posix() for p in html],
            'data_docs_sha256':[digest_file(p) for p in html]}


def run_quality_lab(spark,source:Path,work:Path) -> dict:
    from masar.silver import canonical_rows,delta_artifacts
    from masar.delta_lab import _incoming
    from pyspark.sql import functions as F,types as T
    environment=quality_preflight()
    if environment['issues']: raise EnvironmentUnavailable('; '.join(environment['issues']))
    trusted=completed_day03_table(spark,source,work).select(*BUSINESS_FIELDS)
    trusted_before=canonical_rows(trusted)
    drivers=set(drivers_index(read_csv(source,'drivers.csv')))
    expected=day04_reference(source)
    run_id=uuid.uuid4().hex
    prefix=f'reports/day04_quality/{run_id}'
    clean_policy=evaluate_quality(trusted_before,drivers)
    clean_gx=gx_validate_rows(trusted_before,drivers,workspace_path(work,prefix+'/gx_trusted'),'trusted')
    if not clean_policy['promote_allowed'] or not clean_gx['success']:
        raise AssertionError('Trusted Silver did not pass both policy and GX')
    bad=_incoming(spark,source,work,'quality_cases.csv',1).select(*BUSINESS_FIELDS)
    candidate=trusted.unionByName(bad)
    candidate_path=workspace_path(work,'mini_lakehouse/staging/day04_quality/'+run_id)
    candidate.write.format('delta').mode('errorifexists').save(str(candidate_path))
    candidate=spark.read.format('delta').load(str(candidate_path))
    rows=canonical_rows(candidate)
    mixed_policy=evaluate_quality(rows,drivers)
    mixed_gx=gx_validate_rows(rows,drivers,workspace_path(work,prefix+'/gx_mixed'),'mixed')
    write_json(workspace_path(work,prefix+'/mixed_policy.json'),mixed_policy)
    if mixed_policy['promote_allowed'] or mixed_gx['success']:
        raise AssertionError('Deliberately contaminated candidate unexpectedly passed')
    # Quarantine keeps the complete teaching row and one or more root reasons.
    quarantine_rows=[{'candidate_row':r['candidate_row'],'trip_id':r['trip_id'],
        'reason_codes':r['reason_codes'],'raw_business_json':json.dumps(r['row'],sort_keys=True,ensure_ascii=False),
        'rule_version':QUALITY_RULE_VERSION,'candidate_path':candidate_path.relative_to(work).as_posix()}
        for r in mixed_policy['quarantine']]
    schema=T.StructType([T.StructField('candidate_row',T.LongType()),T.StructField('trip_id',T.StringType()),
        T.StructField('reason_codes',T.ArrayType(T.StringType())),T.StructField('raw_business_json',T.StringType()),
        T.StructField('rule_version',T.StringType()),T.StructField('candidate_path',T.StringType())])
    quarantine_path=workspace_path(work,'mini_lakehouse/quarantine/day04/'+run_id)
    spark.createDataFrame(quarantine_rows,schema).write.format('delta').mode('errorifexists').save(str(quarantine_path))
    # Do not promote a subset from a failed batch. Revalidation creates a separate
    # candidate and receives its own independent GX result before publication.
    accepted_ids=[r['trip_id'] for r in mixed_policy['accepted']]
    filtered=candidate.where(F.col('trip_id').isin(accepted_ids))
    filtered_rows=canonical_rows(filtered)
    filtered_policy=evaluate_quality(filtered_rows,drivers)
    filtered_gx=gx_validate_rows(filtered_rows,drivers,workspace_path(work,prefix+'/gx_rechecked'),'rechecked')
    if not filtered_policy['promote_allowed'] or not filtered_gx['success']:
        raise AssertionError('Rechecked clean candidate did not pass')
    if filtered_rows!=trusted_before:
        raise AssertionError('Rechecked contents changed trusted business data')
    approved_path=workspace_path(work,'mini_lakehouse/silver/validated_day04/'+run_id)
    filtered.write.format('delta').mode('errorifexists').save(str(approved_path))
    approved=spark.read.format('delta').load(str(approved_path))
    current=spark.read.format('delta').load(str(workspace_path(work,'mini_lakehouse/silver/trips')))
    checks={
        'trusted_and_rechecked_pass_gx':clean_gx['success'] and filtered_gx['success'],
        'mixed_candidate_fails_gx':mixed_gx['success'] is False,
        'native_mixed_counts':len(rows)==82 and mixed_policy['accepted_rows']==75 and mixed_policy['rejected_rows']==7,
        'native_reasons_match_reference':mixed_policy['reason_counts']==expected['quality_mixed']['reason_counts'],
        'failed_candidate_not_promoted':mixed_policy['promote_allowed'] is False,
        'quarantine_delta_readback':spark.read.format('delta').load(str(quarantine_path)).count()==7,
        'approved_readback_same_business_contents':canonical_rows(approved)==trusted_before,
        'source_silver_untouched':canonical_rows(current)==trusted_before,
        'data_docs_exist_for_all_three_cases':all(x['data_docs'] for x in [clean_gx,mixed_gx,filtered_gx]),
    }
    if not all(checks.values()): raise AssertionError(checks)
    result={'scope':'DAY04_NATIVE_QUALITY','engine_executed':True,'gx_executed':True,'run_id':run_id,
        'spark_version':spark.version,'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,
        'gx_results':[clean_gx,mixed_gx,filtered_gx],
        'candidate_table':candidate_path.relative_to(work).as_posix(),
        'quarantine_table':quarantine_path.relative_to(work).as_posix(),
        'approved_table':approved_path.relative_to(work).as_posix(),
        'reports':prefix,'approved_business_digest':rows_digest(trusted_before),
        'distribution':city_distribution(filtered_rows,trusted_before),
        'scenario_freshness':{'source_event':expected['source_event_freshness'],
                              'delivery':expected['delivery_freshness'],'as_of':expected['scenario_clock']},
        'artifacts':{'candidate':delta_artifacts(work,candidate_path),'quarantine':delta_artifacts(work,quarantine_path),
                     'approved':delta_artifacts(work,approved_path)},
        'checks':checks,'not_proven':['production-scale quality performance','permissions enforcement','legal compliance certification']}
    write_json(workspace_path(work,prefix+'/quality.json'),result)
    write_json(workspace_path(work,'reports/day04_quality_latest.json'),result)
    return result
