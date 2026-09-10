"""Read actual structured Spark metadata for the pinned dbt-spark catalog.

SHOW TABLE EXTENDED may omit printable column details for Delta relations.
Use the adapter's DESCRIBE TABLE EXTENDED implementation instead. Session
views have no schema and do not belong in the persistent project catalog.
Adapter source: https://github.com/dbt-labs/dbt-spark/blob/v1.9.1/dbt/adapters/spark/impl.py
"""
from contextlib import contextmanager


def describe_catalog_columns(adapter, relation):
    """Yield actual columns for persistent relations, excluding session views."""
    if not relation.schema:
        # Spark lists local temporary views in every schema. They are not
        # persisted project relations; the runner separately requires all six
        # real models and all three real source tables in the final catalog.
        return
    columns = adapter.get_columns_in_relation(relation)
    if not columns:
        raise ValueError(f'No actual columns returned for catalog relation {relation}')
    for column in columns:
        record = column.to_column_dict()
        record['column_name'] = record.pop('column')
        record['column_type'] = record.pop('dtype')
        record['table_database'] = None
        yield record


@contextmanager
def structured_spark_catalog(adapter_type=None):
    """Scope the compatibility override to one serial docs call; always restore."""
    if adapter_type is None:
        from dbt.adapters.spark.impl import SparkAdapter
        adapter_type = SparkAdapter
    original = adapter_type._get_columns_for_catalog
    adapter_type._get_columns_for_catalog = describe_catalog_columns
    try:
        yield
    finally:
        adapter_type._get_columns_for_catalog = original
