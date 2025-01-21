from dataclasses import dataclass, asdict
from random import randint

from utils.data_generators import generate_days_time_series, generate_random_seq
from infrastructure.storage import storage


@dataclass
class Query:
    text: str
    execution_time_ms: int
    number_of_calls: int


def bootstrap_db() -> None:
    query_durations = {}

    for day in generate_days_time_series():
        day_durations = generate_random_seq()
        query_durations[day] = day_durations

    storage["query_durations"] = query_durations
    storage["slowest_queries"] = gen_slowest_queries()
    storage["popular_queries"] = gen_popular_queries()


def gen_slowest_queries() -> list[dict]:
    slowest_queries = [
        Query(
            text="SELECT answer FROM ultimate_questions WHERE question = 'What is the meaning of life, the universe, and everything?';",
            execution_time_ms=42000,
            number_of_calls=1,
        ),
        Query(
            text="SELECT product_name, SUM(quantity) AS total_sold FROM sales GROUP BY product_name ORDER BY total_sold DESC;",
            execution_time_ms=randint(200, 3000),
            number_of_calls=randint(1, 999999),
        ),
        Query(
            text="SELECT category, AVG(price) FROM products GROUP BY category;",
            execution_time_ms=randint(200, 3000),
            number_of_calls=randint(1, 999999),
        ),
        Query(
            text="SELECT name FROM customers WHERE id IN (SELECT customer_id FROM orders);",
            execution_time_ms=randint(200, 3000),
            number_of_calls=randint(1, 999999),
        ),
        Query(
            text="SELECT * FROM orders WHERE client='NillDorMash';",
            execution_time_ms=randint(200, 3000),
            number_of_calls=randint(1, 999999),
        ),
    ]
    return [asdict(d) for d in slowest_queries]


def gen_popular_queries() -> list[dict]:
    slowest_queries = [
        Query(
            text=f"Most populat query of the week {n + 1};",
            execution_time_ms=randint(50, 300),
            number_of_calls=randint(10000, 30000),
        )
        for n in range(5)
    ]
    return [asdict(d) for d in slowest_queries]
