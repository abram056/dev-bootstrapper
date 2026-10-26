"""Reusable analysis helpers for {{project_name}}."""

from __future__ import annotations

from statistics import mean


def summarize(values: list[float]) -> dict[str, float]:
    """Return basic summary statistics for *values*."""
    if not values:
        return {"count": 0, "mean": 0.0, "min": 0.0, "max": 0.0}
    return {
        "count": len(values),
        "mean": mean(values),
        "min": min(values),
        "max": max(values),
    }
