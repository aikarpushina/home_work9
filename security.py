"""
Получение токена для бота
"""


def get_token():
    with open(file="token", mode="r", encoding="utf-8") as f:
        token = f.readline().strip()
    return token
