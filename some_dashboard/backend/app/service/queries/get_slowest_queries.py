from infrastructure.storage import storage


async def get_slowest_queries() -> dict:
    slowest_queries = sorted(
        storage["slowest_queries"], key=lambda x: x["execution_time_ms"], reverse=True
    )

    result = {
        "title": f"Top {len(slowest_queries)} slowest queries",
        "headers": ["Query", "Execution Time (ms)", "Number of calls"],
        "rows": [list(row.values()) for row in slowest_queries],
    }
    return result
