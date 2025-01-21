from infrastructure.storage import storage
from utils.stat import calculate_percentile

BASE_QUERY_TRESHOLD = 110
CRITICAL_QUERY_TRESHOLD = 145


async def get_query_durations() -> dict:
    queries_data = storage["query_durations"]
    chart_data = {
        "title": "Query durations (ms)",
        "labels": [day for day in queries_data.keys()],
        "lines": [],
    }

    chart_data["lines"].append(
        {
            "label": "critical",
            "data": [CRITICAL_QUERY_TRESHOLD for _ in range(len(queries_data.keys()))],
            "lineFormat": {
                "borderColor": "red",
                "borderDash": [5, 5],  # пунктир
                "pointRadius": 0,
            },
        }
    )

    chart_data["lines"].append(
        {
            "label": "base",
            "data": [BASE_QUERY_TRESHOLD for _ in range(len(queries_data.keys()))],
            "lineFormat": {
                "borderColor": "blue",
                "borderDash": [5, 5],  # пунктир
                "pointRadius": 0,
            },
        }
    )

    q95 = []
    q75 = []
    q50 = []

    for _, values in queries_data.items():
        sorted_values = sorted(values)
        q95.append(calculate_percentile(sorted_values, 95))
        q75.append(calculate_percentile(sorted_values, 75))
        q50.append(calculate_percentile(sorted_values, 50))

    chart_data["lines"].append(
        {
            "label": "q95",
            "data": q95,
            "lineFormat": {
                "borderColor": "green",
            },
        }
    )
    chart_data["lines"].append(
        {
            "label": "q75",
            "data": q75,
            "lineFormat": {
                "borderColor": "orange",
            },
        }
    )
    chart_data["lines"].append(
        {
            "label": "q50",
            "data": q50,
            "lineFormat": {
                "borderColor": "brown",
            },
        }
    )
    return chart_data
