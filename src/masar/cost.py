"""Hypothetical cost arithmetic, not prices or measured Spark performance."""
from decimal import Decimal, InvalidOperation, localcontext

DEFAULTS = {
    "days": "30", "hours_per_day": "24", "cores": "4",
    "price_per_core_hour": "0.50", "storage_gib": "100",
    "storage_price_per_gib_month": "0.20", "work_hours_per_day": "2",
    "startup_hours_per_day": "0.25", "scheduled_extra_monthly": "30",
    "always_on_extra_monthly": "0",
}

def evaluate_cost(inputs: dict) -> dict:
    """Illustrative budget only; no cloud provider or Spark measurement."""
    if set(inputs) != set(DEFAULTS):
        raise ValueError("Input keys must match DEFAULTS")
    try:
        p = {key: Decimal(str(value)) for key, value in inputs.items()}
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("All inputs must be numeric") from exc
    if any(not value.is_finite() or value < 0 for value in p.values()):
        raise ValueError("Inputs must be finite and non-negative")
    if p["days"] <= 0 or p["cores"] <= 0 or not (0 < p["hours_per_day"] <= 24):
        raise ValueError("Days, cores and available hours must be positive")
    if p["days"] != p["days"].to_integral_value() or p["cores"] != p["cores"].to_integral_value():
        raise ValueError("Days and cores must be whole numbers")
    work = p["work_hours_per_day"]
    startup = p["startup_hours_per_day"]
    if work > 0 and work + startup > p["hours_per_day"]:
        raise ValueError("Work plus startup exceeds available daily hours")
    with localcontext() as context:
        context.prec = 28
        always_hours = p["days"] * p["hours_per_day"]
        scheduled_hours = p["days"] * (work + startup if work > 0 else Decimal(0))
        rate = p["cores"] * p["price_per_core_hour"]
        storage = p["storage_gib"] * p["storage_price_per_gib_month"]
        always_compute = always_hours * rate
        scheduled_compute = scheduled_hours * rate
        always_total = always_compute + storage + p["always_on_extra_monthly"]
        scheduled_total = scheduled_compute + storage + p["scheduled_extra_monthly"]
        difference = always_total - scheduled_total
        threshold = ((always_compute + p["always_on_extra_monthly"] - p["scheduled_extra_monthly"])
                     / rate / p["days"] - startup) if rate else None
        return {
            "unit": "TU (hypothetical teaching units; not currency)",
            "always_on_hours": always_hours, "scheduled_hours": scheduled_hours,
            "always_on_compute": always_compute, "scheduled_compute": scheduled_compute,
            "storage_each": storage, "always_on_total": always_total,
            "scheduled_total": scheduled_total, "difference": difference,
            "reduction_fraction": difference / always_total if always_total else None,
            "break_even_work_hours_per_day": threshold,
        }

def serializable(result: dict) -> dict:
    return {key: str(value) if isinstance(value, Decimal) else value for key, value in result.items()}

WORKLOADS = ["0", "1", "2", "4", "8", "12", "18", "23", "23.25", "23.75"]

def cost_report() -> dict:
    base = evaluate_cost(DEFAULTS)
    sensitivity = []
    for hours in WORKLOADS:
        result = evaluate_cost({**DEFAULTS, "work_hours_per_day": hours})
        sensitivity.append({"work_hours_per_day": hours,
            **{key: str(result[key]) for key in ("always_on_total", "scheduled_total", "difference")}})
    return {"scope": "ILLUSTRATIVE_COST_ARITHMETIC_ONLY", "spark_benchmark_executed": False,
        "assumptions": DEFAULTS, "base": serializable(base), "sensitivity": sensitivity,
        "exclusions": ["provider prices", "tax", "egress", "request fees", "latency SLA", "real Spark benchmark", "production sizing"]}
