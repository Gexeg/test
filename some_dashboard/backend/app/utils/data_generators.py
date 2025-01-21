from datetime import datetime
from datetime import timedelta
from random import randint

DATE_FORMAT = "%d.%m.%y"


def generate_random_seq(min_int: int = 1, max_int: int = 150, len: int = 100):
    return [randint(min_int, max_int) for _ in range(len)]


def generate_days_time_series(days: int = 10) -> str:
    base_time = datetime.now() - timedelta(days=days)
    time_series = [
        (base_time + timedelta(days=i)).strftime(DATE_FORMAT) for i in range(days)
    ]
    return time_series
