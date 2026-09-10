"""Catalog unit checks; native dbt execution is validated separately."""
import sys
from pathlib import Path
import unittest
from types import SimpleNamespace
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from masar.dbt_catalog import describe_catalog_columns, structured_spark_catalog


class Relation(str):
    schema = 'example'


class Column:
    def to_column_dict(self):
        return {'column': 'trip_id', 'dtype': 'string', 'column_index': 0,
                'table_schema': 'example', 'table_name': 'silver_trips',
                'table_type': 'table', 'table_database': None}


class Adapter:
    def get_columns_in_relation(self, relation):
        self.observed_relation = relation
        return [Column()]

    def _get_columns_for_catalog(self, relation):
        return []


class CatalogTests(unittest.TestCase):
    def test_uses_structured_native_schema(self):
        adapter = Adapter()
        rows = list(describe_catalog_columns(adapter, Relation('example.silver_trips')))
        self.assertEqual(adapter.observed_relation, 'example.silver_trips')
        self.assertEqual(rows[0]['column_name'], 'trip_id')
        self.assertEqual(rows[0]['column_type'], 'string')
        self.assertEqual(rows[0]['table_schema'], 'example')
        self.assertNotIn('dtype', rows[0])

    def test_empty_persistent_schema_fails_instead_of_inventing_columns(self):
        adapter = Adapter()
        adapter.get_columns_in_relation = lambda relation: []
        with self.assertRaisesRegex(ValueError, 'No actual columns'):
            list(describe_catalog_columns(adapter, Relation('missing')))

    def test_session_temporary_views_are_not_persistent_catalog_tables(self):
        adapter = Adapter()
        for schema in ('', None):
            relation = SimpleNamespace(schema=schema, identifier='silver_trips__dbt_tmp')
            self.assertEqual(list(describe_catalog_columns(adapter, relation)), [])
        self.assertFalse(hasattr(adapter, 'observed_relation'))

    def test_context_restores_the_original_method(self):
        original = Adapter._get_columns_for_catalog
        with structured_spark_catalog(Adapter):
            self.assertIs(Adapter._get_columns_for_catalog, describe_catalog_columns)
            self.assertEqual(len(list(Adapter()._get_columns_for_catalog(Relation('table')))), 1)
        self.assertIs(Adapter._get_columns_for_catalog, original)

    def test_restoration_also_happens_after_error(self):
        original = Adapter._get_columns_for_catalog
        with self.assertRaisesRegex(RuntimeError, 'test failure'):
            with structured_spark_catalog(Adapter):
                raise RuntimeError('test failure')
        self.assertIs(Adapter._get_columns_for_catalog, original)


if __name__ == '__main__':
    unittest.main()
