"""Dependency-ordered native integration; a failed stage blocks its descendants."""
from __future__ import annotations
from pathlib import Path
from typing import Callable
import json
import os
from datetime import datetime, timezone
from masar.native_contracts import validate_stage_result
from masar.release_evidence import implementation_digest, seal_inventory
from masar.runtime import inspect_environment,EnvironmentUnavailable,start_spark
from masar.workspace import new_workspace,workspace_path,write_json,record_bronze_success,DATASET_MANIFEST_SHA256


def dependency_preflight() -> dict:
    from masar.streaming import stream_preflight
    from masar.quality_gate import quality_preflight
    components={'spark_delta':inspect_environment(),'kafka':stream_preflight(),'gx':quality_preflight()}
    issues=[issue for report in components.values() for issue in report['issues']]
    return {'scope':'INTEGRATION_DEPENDENCIES_ONLY','engine_executed':False,'components':components,
            'issues':issues,'status':'BLOCKED_DEPENDENCIES' if issues else 'PREREQUISITES_PRESENT_NOT_RUNTIME_PROOF'}


def execute_steps(steps: list[tuple[str,Callable[[],dict]]], journal: Path) -> dict:
    """Generic sequencing helper. Its unit tests do not prove any data engine."""
    names=[name for name,_ in steps]
    if not names or len(names)!=len(set(names)) or not all(isinstance(n,str) and n for n in names):
        raise ValueError('Use uniquely named non-empty ordered stages')
    state={'scope':'ORDERED_STAGE_JOURNAL','status':'RUNNING','stages':[]}
    for name,action in steps:
        entry={'stage':name,'status':'RUNNING'};state['stages'].append(entry);write_json(journal,state)
        try:
            result=action()
            validate_stage_result(name, result)
            entry.update(status='PASSED',result=result)
            write_json(journal,state)
        except Exception as exc:
            entry.update(status='FAILED',error_type=type(exc).__name__,message=str(exc))
            state.update(status='FAILED',blocked_stages=names[len(state['stages']):])
            write_json(journal,state)
            raise
    state['status']='PASSED';state['blocked_stages']=[];write_json(journal,state)
    return state


def run_pipeline(root:Path) -> dict:
    root=Path(root).resolve()
    preflight=dependency_preflight()
    if preflight['issues']: raise EnvironmentUnavailable('; '.join(preflight['issues']))
    from masar.bronze import build_bronze
    from masar.benchmark import benchmark
    from masar.silver import run_staging_lab,run_incremental_lab
    from masar.delta_lab import run_transactions_lab,run_maintenance_lab
    from masar.streaming import run_stream_lab
    from masar.quality_gate import run_quality_lab
    from masar.serving import run_recovery_exercise,run_serving_lab
    work=new_workspace(root,'integration');source=root/'data/masar-small-v1'
    spark=None
    report={'scope':'MASAR_NATIVE_INTEGRATION','status':'RUNNING','engine_executed':False,
        'workspace':work.relative_to(root).as_posix(),'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,
        'run_id':json.loads((work/'.masar-workspace.json').read_text())['run_id'],
        'process_id':os.getpid(),'started_at_utc':datetime.now(timezone.utc).isoformat(),
        'implementation_sha256':implementation_digest(root),
        'dbt_executed':False,'all_course_requirements_verified':False,
        'limits':['dbt adapter validation remains separate','one local integration run is not two independent environments',
                  'no production or publication approval']}
    target=workspace_path(work,'reports/integration.json')
    try:
        spark=start_spark(work,kafka=True)
        def bronze():
            result=build_bronze(spark,source,work);record_bronze_success(root,work);return result
        steps=[('lab01_bronze',bronze),('lab02_scan',lambda:benchmark(spark,source,work)),
            ('lab03a_staging',lambda:run_staging_lab(spark,source,work)),
            ('lab03b_silver',lambda:run_incremental_lab(spark,source,work)),
            ('lab04a_transactions',lambda:run_transactions_lab(spark,source,work)),
            ('lab04b_maintenance',lambda:run_maintenance_lab(spark,source,work)),
            ('lab05_streaming',lambda:run_stream_lab(spark,source,work)),
            ('lab06_quality',lambda:run_quality_lab(spark,source,work)),
            ('lab07_gold_recovery',lambda:run_recovery_exercise(spark,source,work)),
            ('lab08_serving',lambda:run_serving_lab(spark,source,work))]
        state=execute_steps(steps,workspace_path(work,'reports/integration_stages.json'))
        report.update(status='PASSED_NATIVE_PATH_DBT_NOT_VALIDATED',engine_executed=True,
                      stage_names=[s['stage'] for s in state['stages']])
    except Exception as exc:
        report.update(status='FAILED',engine_started=spark is not None,error_type=type(exc).__name__,message=str(exc))
        raise
    finally:
        if spark is not None:
            try:spark.stop()
            except Exception as exc:
                report.update(status='FAILED_SHUTDOWN',shutdown_error=str(exc),finished_at_utc=datetime.now(timezone.utc).isoformat())
                write_json(target,report)
                raise
        report['finished_at_utc']=datetime.now(timezone.utc).isoformat()
        write_json(target,report)
        if report['status']=='PASSED_NATIVE_PATH_DBT_NOT_VALIDATED':
            seal_inventory(work)
    return report
