import random
import re
import uuid

FIRST_NAMES = [
    "Ana",
    "Bruno",
    "Carla",
    "Diego",
    "Eduarda",
    "Felipe",
    "Giovana",
    "Henrique",
]

PRODUCT_NAMES = [
    "Mouse Gamer",
    "Teclado Mecânico",
    "Headset Pro",
    "Webcam HD",
    "Monitor UltraWide",
    "SSD NVMe",
]


def random_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {uuid.uuid4().hex[:6]}"


def random_product() -> str:
    return f"{random.choice(PRODUCT_NAMES)} {uuid.uuid4().hex[:8]}"


def random_email() -> str:
    first_name = random.choice(FIRST_NAMES).lower()
    sanitized = re.sub(r"[^a-z0-9]", "", first_name)
    suffix = uuid.uuid4().hex[:8]
    return f"{sanitized}.{suffix}@gmail.com"


def random_password() -> str:
    return f"Senha@{uuid.uuid4().hex[:10]}"
