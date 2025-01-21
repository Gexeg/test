from infrastructure.storage import storage


async def get_popular_queries() -> dict:
    slowest_queries = sorted(
        storage["popular_queries"], key=lambda x: x["number_of_calls"], reverse=True
    )

    result = {
        "title": f"Top {len(slowest_queries)} popular queries",
        "headers": ["Query", "Execution Time (ms)", "Number of calls"],
        "rows": [list(row.values()) for row in slowest_queries],
    }
    return result
