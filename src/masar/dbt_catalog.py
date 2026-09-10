"""Generate dbt catalog columns from DESCRIBE TABLE EXTENDED, not display text.

The pinned dbt-spark adapter normally parses SHOW TABLE EXTENDED information
with a regular expression. Delta relations can omit the printable schema even
though the real table has columns. During the serial docs invocation, use the
adapter's existing structured DESCRIBE implementation for every relation.
No table, column, type, or successful validation is synthesized.
Adapter source: https://github.com/dbt-labs/dbt-spark/blob/v1.9.1/dbt/adapters/spark/impl.py
"""
from contextlib import contextmanager


def describe_catalog_columns(adapter, relation):
    """Yield native catalog records using the adapter's actual DESCRIBE result."""
    columns = adapter.get_columns_in_relation(relation)
    if not columns:
        raise ValueError(f'No actual columns returned for catalog relation {relation}')
    for column in columns:
        record = column.to_column_dict()
        record['column_name'] = record.pop('column')
        record['column_type'] = record.pop('dtype')
        record['table_database'] = None  # dbt-spark uses schema, not a separate database.
        yield record


@contextmanager
def structured_spark_catalog(adapter_type=None):
    """Scope the compatibility override to one docs call and always restore it.

    The course invokes dbt serially in its isolated worker process. This is not
    intended for concurrent independent dbt runners within a shared process.
    """
    if adapter_type is None:
        from dbt.adapters.spark.impl import SparkAdapter
        adapter_type = SparkAdapter
    original = adapter_type._get_columns_for_catalog
    adapter_type._get_columns_for_catalog = describe_catalog_columns
    try:
        yield
    finally:
        adapter_type._get_columns_for_catalog = original
