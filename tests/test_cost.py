from pathlib import Path
from decimal import Decimal
import sys, unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from masar.cost import DEFAULTS,evaluate_cost,cost_report
class CostTests(unittest.TestCase):
    def test_base_totals(self):
        r=evaluate_cost(DEFAULTS);self.assertEqual((r["always_on_total"],r["scheduled_total"]),(Decimal(1460),Decimal(185)))
    def test_equal_storage(self):self.assertEqual(evaluate_cost(DEFAULTS)["storage_each"],Decimal(20))
    def test_break_even(self):self.assertEqual(evaluate_cost({**DEFAULTS,"work_hours_per_day":"23.25"})["difference"],0)
    def test_counterexample(self):self.assertEqual(evaluate_cost({**DEFAULTS,"work_hours_per_day":"23.75"})["difference"],Decimal(-30))
    def test_zero_work(self):self.assertEqual(evaluate_cost({**DEFAULTS,"work_hours_per_day":"0"})["scheduled_hours"],0)
    def test_zero_rate(self):self.assertIsNone(evaluate_cost({**DEFAULTS,"price_per_core_hour":"0"})["break_even_work_hours_per_day"])
    def test_zero_baseline(self):self.assertIsNone(evaluate_cost({**DEFAULTS,"price_per_core_hour":"0","storage_gib":"0"})["reduction_fraction"])
    def test_invalid_inputs(self):
        for change in [{"cores":"-1"},{"days":"0"},{"storage_gib":"NaN"},{"storage_gib":"Infinity"},{"cores":"1.5"},{"days":"1.5"},{"work_hours_per_day":"24"},{"hours_per_day":"25"},{"cores":"abc"}]:
            with self.subTest(change=change),self.assertRaises(ValueError):evaluate_cost({**DEFAULTS,**change})
    def test_missing_input(self):
        with self.assertRaises(ValueError):evaluate_cost({"days":"30"})
    def test_unknown_input(self):
        with self.assertRaises(ValueError):evaluate_cost({**DEFAULTS,"unknown":"1"})
    def test_sensitivity_length_and_boundary(self):
        r=cost_report();self.assertEqual(len(r["sensitivity"]),10);self.assertFalse(r["spark_benchmark_executed"])
    def test_deterministic_result(self):self.assertEqual(cost_report(),cost_report())
