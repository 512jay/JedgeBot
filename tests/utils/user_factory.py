# /tests/utils/user_factory.py

import random
import string


def random_email() -> str:
    return f"user_{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com"


def random_password(length: int = 12) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
