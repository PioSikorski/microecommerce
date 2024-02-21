import random
import string


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_float() -> float:
    return round(random.random(), 2)


def random_int() -> int:
    return random.randint(5, 1000)


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"