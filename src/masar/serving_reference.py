"""Day 5 independent serving oracle. Standard-library calculations are NOT Delta.

The approved small fixture represents three cities, not precise zones. AI uses
scenario availability as well as event time. No future labels are manufactured.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
from zoneinfo import ZoneInfo
from masar.delta_reference import day03_reference
from masar.silver_reference import read_csv, drivers_index, parse_timestamp
from masar.trust_reference import GPS_FILES, events_from_source, unique_events, event_contract, evaluate_quality
from masar.workspace import require_fixed_dataset, rows_digest, DATASET_MANIFEST_SHA256

AS_OF = '2026-06-04T03:05:00Z'
TZ = ZoneInfo('Asia/Riyadh')
ZONE_KEYS = {'Riyadh': 'Z_RIYADH', 'Jeddah': 'Z_JEDDAH', 'Dammam': 'Z_DAMMAM'}
TABLE_COLUMNS = {
    'gold.zone_hourly_demand': ('zone_key','hour_utc','hour_local','trip_count','total_fare_sar','total_duration_seconds'),
    'gold.driver_daily': ('driver_key','trip_date_local','trip_count','total_fare_sar','total_duration_seconds'),
    'bi.dim_zone': ('zone_key','city','zone_resolution'),
    'bi.dim_driver': ('driver_key','driver_id','vehicle_type'),
    'bi.dim_date': ('date_key','date_local','year','month','day'),
    'bi.fact_trips': ('trip_id','driver_key','zone_key','date_key','start_utc','fare_sar','distance_km','duration_seconds','gps_event_count'),
    'ai.zone_hourly_features': ('zone_key','as_of_utc','prediction_hour_utc','history_window_start_utc','completed_trips_24h','avg_duration_seconds_24h','history_available','max_source_available_at_utc'),
    'ai.zone_hourly_labels': ('zone_key','prediction_hour_utc','target_trip_count','label_status','label_available_at_utc'),
}
TABLE_KEYS = {
    'gold.zone_hourly_demand': ('zone_key','hour_utc'),
    'gold.driver_daily': ('driver_key','trip_date_local'),
    'bi.dim_zone': ('zone_key',), 'bi.dim_driver': ('driver_key',), 'bi.dim_date': ('date_key',),
    'bi.fact_trips': ('trip_id',), 'ai.zone_hourly_features': ('zone_key','as_of_utc','prediction_hour_utc'),
    'ai.zone_hourly_labels': ('zone_key','prediction_hour_utc'),
}
FEATURE_INPUTS = ('zone_key','completed_trips_24h','avg_duration_seconds_24h','history_available')
FORBIDDEN_FEATURES = {'target_trip_count','fare_sar','end_utc','gps_event_count','trip_id','driver_id','latitude','longitude','location'}


def utc_text(value):
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')


def money(value: Decimal) -> str:
    return format(value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP), '.2f')


def availability_index(source: Path) -> dict[tuple[str,int], str]:
    """Earliest delivery of each revision; replay is not newly available history."""
    require_fixed_dataset(source)
    schedule = json.loads((source/'scenario_schedule.json').read_text(encoding='utf-8'))
    index = {}
    for phase in schedule['phases']:
        if phase['name'] == 'quality':
            continue
        dt = parse_timestamp(phase['available_at'])
        if dt is None:
            raise ValueError('Availability timestamps must include timezone')
        for raw in read_csv(source, phase['file']):
            key = (raw['trip_id'].strip(), phase['revision'])
            if key not in index or dt < parse_timestamp(index[key]):
                index[key] = utc_text(dt)
    return index


def validate_feature_inputs(columns: list[str] | tuple[str,...]) -> None:
    if len(columns) != len(set(columns)) or set(columns) != set(FEATURE_INPUTS):
        raise ValueError('Use only the documented model-input allowlist; IDs, audit times and labels are not features')


def validate_tables(tables: dict[str,list[dict]]) -> dict:
    if set(tables) != set(TABLE_COLUMNS):
        raise ValueError('Serving release must contain exactly the eight contracted tables')
    checks = {}
    for name, columns in TABLE_COLUMNS.items():
        rows = tables[name]
        if not isinstance(rows, list) or not rows:
            raise ValueError('Empty or invalid serving table: '+name)
        if any(not isinstance(row,dict) or set(row) != set(columns) for row in rows):
            raise ValueError('Unexpected columns in '+name)
        keys = [tuple(row[k] for k in TABLE_KEYS[name]) for row in rows]
        if any(any(k is None or k == '' for k in key) for key in keys) or len(keys) != len(set(keys)):
            raise ValueError('Missing or duplicate serving key: '+name)
        checks[name+'_schema_and_keys'] = True
    facts = tables['bi.fact_trips']
    if len(facts) != 75:
        raise ValueError('The approved fixture requires 75 fact trips')
    for dimension, key in [('bi.dim_zone','zone_key'),('bi.dim_driver','driver_key'),('bi.dim_date','date_key')]:
        ids = {r[key] for r in tables[dimension]}
        if any(f[key] not in ids for f in facts):
            raise ValueError('Orphan fact key: '+key)
    if any(type(f['gps_event_count']) is not int or f['gps_event_count'] < 0 for f in facts):
        raise ValueError('Invalid event count')
    # Check each group as well as the grand total.
    expected_hourly, expected_daily = defaultdict(list), defaultdict(list)
    for fact in facts:
        start = parse_timestamp(fact['start_utc'])
        if start is None or type(fact['duration_seconds']) is not int or fact['duration_seconds'] <= 0:
            raise ValueError('Invalid fact timestamp or duration')
        local_date = start.astimezone(TZ).date().isoformat()
        if fact['date_key'] != int(local_date.replace('-','')):
            raise ValueError('Fact date does not match the local start-date contract')
        expected_hourly[(fact['zone_key'],utc_text(start.replace(minute=0,second=0)))].append(fact)
        expected_daily[(fact['driver_key'],local_date)].append(fact)
    for name, expected in [('gold.zone_hourly_demand',expected_hourly),('gold.driver_daily',expected_daily)]:
        actual = {tuple(r[k] for k in TABLE_KEYS[name]):r for r in tables[name]}
        if set(actual) != set(expected):
            raise ValueError('Gold group keys differ from fact grain: '+name)
        for key, group in expected.items():
            row = actual[key]
            if (type(row['trip_count']) is not int or row['trip_count'] != len(group)
                or Decimal(row['total_fare_sar']) != sum(Decimal(r['fare_sar']) for r in group)
                or row['total_duration_seconds'] != sum(r['duration_seconds'] for r in group)):
                raise ValueError('Gold group measures differ from facts: '+name)
            if name == 'gold.zone_hourly_demand' and row['hour_local'] != parse_timestamp(key[1]).astimezone(TZ).isoformat():
                raise ValueError('Local hour display differs from UTC hour')
    if {(r['city'],r['zone_key'],r['zone_resolution']) for r in tables['bi.dim_zone']} != {(city,key,'city_proxy') for city,key in ZONE_KEYS.items()}:
        raise ValueError('City-proxy dimension mapping changed')
    if any(r['driver_key'] != r['driver_id'] for r in tables['bi.dim_driver']):
        raise ValueError('The teaching dimension uses the documented natural driver key')
    fare = sum(Decimal(f['fare_sar']) for f in facts)
    duration = sum(f['duration_seconds'] for f in facts)
    for name in ('gold.zone_hourly_demand','gold.driver_daily'):
        if (sum(r['trip_count'] for r in tables[name]) != len(facts)
                or sum(Decimal(r['total_fare_sar']) for r in tables[name]) != fare
                or sum(r['total_duration_seconds'] for r in tables[name]) != duration):
            raise ValueError('Gold/fact reconciliation failed: '+name)
    if fare != Decimal('1880.60') or sum(f['gps_event_count'] for f in facts) != 217:
        raise ValueError('Approved fixture totals changed')
    zones = {r['zone_key'] for r in tables['bi.dim_zone']}
    features, labels = tables['ai.zone_hourly_features'], tables['ai.zone_hourly_labels']
    if {r['zone_key'] for r in features} != zones or len(features) != 3 or len(labels) != 3:
        raise ValueError('Each known zone needs one forecast input and one label-status row')
    fkeys = {(r['zone_key'],r['prediction_hour_utc']) for r in features}
    if fkeys != {(r['zone_key'],r['prediction_hour_utc']) for r in labels}:
        raise ValueError('Feature/label entity-time keys do not align')
    for f in features:
        cutoff, horizon, start = [parse_timestamp(f[k]) for k in ('as_of_utc','prediction_hour_utc','history_window_start_utc')]
        if cutoff is None or horizon is None or start is None or start != cutoff-timedelta(hours=24):
            raise ValueError('Invalid feature window')
        if horizon != cutoff.replace(minute=0,second=0)+timedelta(hours=1):
            raise ValueError('Forecast horizon must be the next complete hour')
        available = parse_timestamp(f['max_source_available_at_utc'])
        if available is not None and available > cutoff:
            raise ValueError('Feature leaks future availability')
        if type(f['completed_trips_24h']) is not int or f['completed_trips_24h'] < 0:
            raise ValueError('Invalid historical count')
        if f['history_available'] is not (f['completed_trips_24h'] > 0):
            raise ValueError('History flag inconsistent')
        if f['completed_trips_24h'] == 0:
            if f['avg_duration_seconds_24h'] is not None or f['max_source_available_at_utc'] is not None:
                raise ValueError('Missing history must stay explicitly unavailable')
        elif f['avg_duration_seconds_24h'] is None or available is None:
            raise ValueError('Historical evidence missing')
    if any(r['label_status'] != 'UNOBSERVED' or r['target_trip_count'] is not None or r['label_available_at_utc'] is not None for r in labels):
        raise ValueError('This fixed fixture has no future ground truth; do not invent zero targets')
    checks.update(fact_grain_75=True, foreign_keys_valid=True, gold_fact_totals_match=True,
                  events_aggregated_before_join=True, group_grains_reconcile=True, labels_not_fabricated=True,
                  feature_availability_checked=True, feature_label_keys_aligned=True)
    return checks


def tables_from_trusted(trips: list[dict], events: list[dict], source: Path, *, as_of: str = AS_OF) -> dict:
    """Independent, bounded derivation. Not a native Spark implementation."""
    require_fixed_dataset(source)
    if not trips or len(trips)>500 or len(events)>500:
        raise ValueError('Use the bounded approved fixture')
    drivers = drivers_index(read_csv(source,'drivers.csv'))
    gate = evaluate_quality(trips,set(drivers))
    if not gate['promote_allowed']:
        raise ValueError('Only a validated 75-trip snapshot can feed Gold')
    unique = unique_events(events)
    ids = {r['trip_id'] for r in trips}
    if any(event_contract(e,ids) for e in unique):
        raise ValueError('Event contract or relationship failed')
    cutoff = parse_timestamp(as_of)
    if cutoff is None:
        raise ValueError('Prediction cutoff must be a timezone-aware timestamp')
    available = availability_index(source)
    window_start, horizon = cutoff-timedelta(hours=24), cutoff.replace(minute=0,second=0)+timedelta(hours=1)
    counts = Counter(e['trip_id'] for e in unique)
    hourly, daily = defaultdict(list), defaultdict(list)
    facts, history = [], defaultdict(list)
    for trip in sorted(trips,key=lambda r:r['trip_id']):
        start = parse_timestamp(trip['start_utc']); end = parse_timestamp(trip['end_utc'])
        zone = ZONE_KEYS[trip['city']]
        hourly[(zone,utc_text(start.replace(minute=0,second=0)))].append(trip)
        daily[(trip['driver_id'],trip['trip_date_local'])].append(trip)
        facts.append(dict(trip_id=trip['trip_id'],driver_key=trip['driver_id'],zone_key=zone,
            date_key=int(trip['trip_date_local'].replace('-','')),start_utc=trip['start_utc'],
            fare_sar=trip['fare_sar'],distance_km=trip['distance_km'],duration_seconds=trip['duration_seconds'],
            gps_event_count=counts[trip['trip_id']]))
        avail = available.get((trip['trip_id'],trip['source_revision']))
        if avail is None:
            raise ValueError('Source revision lacks availability metadata')
        if window_start <= end < cutoff and parse_timestamp(avail) <= cutoff:
            history[zone].append((trip,avail))
    tables = {name:[] for name in TABLE_COLUMNS}
    def measures(rows):
        return dict(trip_count=len(rows),total_fare_sar=money(sum((Decimal(r['fare_sar']) for r in rows),Decimal(0))),
                    total_duration_seconds=sum(r['duration_seconds'] for r in rows))
    for (zone,hour), rows in sorted(hourly.items()):
        tables['gold.zone_hourly_demand'].append(dict(zone_key=zone,hour_utc=hour,
            hour_local=parse_timestamp(hour).astimezone(TZ).isoformat(),**measures(rows)))
    for (driver,date),rows in sorted(daily.items()):
        tables['gold.driver_daily'].append(dict(driver_key=driver,trip_date_local=date,**measures(rows)))
    tables['bi.fact_trips'] = facts
    tables['bi.dim_zone'] = [dict(zone_key=key,city=city,zone_resolution='city_proxy') for city,key in sorted(ZONE_KEYS.items())]
    tables['bi.dim_driver'] = [dict(driver_key=key,driver_id=key,vehicle_type=value['vehicle_type']) for key,value in sorted(drivers.items())]
    for date in sorted({r['trip_date_local'] for r in trips}):
        year,month,day = map(int,date.split('-'))
        tables['bi.dim_date'].append(dict(date_key=year*10000+month*100+day,date_local=date,year=year,month=month,day=day))
    for zone in sorted(ZONE_KEYS.values()):
        past = history[zone]
        average = money(Decimal(sum(t['duration_seconds'] for t,_ in past))/len(past)) if past else None
        tables['ai.zone_hourly_features'].append(dict(zone_key=zone,as_of_utc=utc_text(cutoff),
            prediction_hour_utc=utc_text(horizon),history_window_start_utc=utc_text(window_start),
            completed_trips_24h=len(past),avg_duration_seconds_24h=average,history_available=bool(past),
            max_source_available_at_utc=max((a for _,a in past),default=None)))
        tables['ai.zone_hourly_labels'].append(dict(zone_key=zone,prediction_hour_utc=utc_text(horizon),
            target_trip_count=None,label_status='UNOBSERVED',label_available_at_utc=None))
    for name in tables:
        tables[name] = sorted(tables[name],key=lambda r:tuple(r[k] for k in TABLE_KEYS[name]))
    validate_tables(tables)
    return tables


def independent_sql_check(tables: dict) -> dict:
    """SQLite is used ONLY to recompute BI sums independently, never as a Lakehouse."""
    import sqlite3
    connection = sqlite3.connect(':memory:')
    try:
        connection.execute('CREATE TABLE facts (trip_id TEXT PRIMARY KEY,zone_key TEXT,driver_key TEXT,date_key INTEGER,fare_minor INTEGER,duration_seconds INTEGER,events INTEGER)')
        connection.executemany('INSERT INTO facts VALUES (?,?,?,?,?,?,?)',[
            (r['trip_id'],r['zone_key'],r['driver_key'],r['date_key'],int(Decimal(r['fare_sar'])*100),r['duration_seconds'],r['gps_event_count'])
            for r in tables['bi.fact_trips']])
        total = connection.execute('SELECT COUNT(*),SUM(fare_minor),SUM(duration_seconds),SUM(events) FROM facts').fetchone()
        grouped = connection.execute('SELECT zone_key,COUNT(*),SUM(fare_minor) FROM facts GROUP BY zone_key ORDER BY zone_key').fetchall()
        daily = connection.execute('SELECT driver_key,date_key,COUNT(*),SUM(fare_minor) FROM facts GROUP BY driver_key,date_key ORDER BY driver_key,date_key').fetchall()
        expected_daily=[(r['driver_key'],int(r['trip_date_local'].replace('-','')),r['trip_count'],int(Decimal(r['total_fare_sar'])*100)) for r in tables['gold.driver_daily']]
        if daily != expected_daily: raise AssertionError('Independent SQL daily reconciliation failed')
        return {'scope':'INDEPENDENT_SQL_RECONCILIATION_NOT_SPARK', 'trip_count':total[0],
                'fare_minor':total[1],'duration_seconds':total[2],'gps_events':total[3],
                'zone_totals':[dict(zone_key=z,trip_count=n,fare_minor=f) for z,n,f in grouped],
                'daily_group_reconciliation':True}
    finally:
        connection.close()


def day05_reference(source: Path) -> dict:
    trips = day03_reference(source)['expected_corrected_rows']
    events = [event for name in GPS_FILES for event in events_from_source(source,name)]
    tables = tables_from_trusted(trips,events,source)
    checks = validate_tables(tables)
    sql = independent_sql_check(tables)
    checks['independent_sql_totals'] = sql['trip_count']==75 and sql['fare_minor']==188060 and sql['gps_events']==217
    checks['feature_allowlist'] = not set(FEATURE_INPUTS)&FORBIDDEN_FEATURES
    if not all(checks.values()): raise AssertionError(checks)
    return {'scope':'DAY05_SOURCE_EXPECTATIONS_ONLY','engine_executed':False,
        'dataset_manifest_sha256':DATASET_MANIFEST_SHA256,'as_of_utc':AS_OF,
        'tables':tables,'row_counts':{k:len(v) for k,v in tables.items()},
        'content_digests':{k:rows_digest(v) for k,v in tables.items()},
        'reconciliation':sql,'feature_inputs':list(FEATURE_INPUTS),
        'label_status':'UNOBSERVED_FUTURE_NOT_ZERO','checks':checks,
        'not_proven':['native Delta materialization','full pipeline execution','dbt adapter execution',
            'live feature serving','model accuracy','Power BI connector execution','production scalability','publication approval']}
