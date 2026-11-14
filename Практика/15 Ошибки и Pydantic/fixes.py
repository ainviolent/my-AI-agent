import logging
from pydantic import BaseModel

# Задание 23: двоеточия после try и except.
try:
    print('Запрос')
except Exception as error:
    print('Ошибка', type(error).__name__)

# Задание 24: запятая между аргументами.
logging.basicConfig(filename='app.log', level=logging.INFO)

# Задание 25: двоеточие после имени класса и типы полей.
class Result(BaseModel):
    category: str
    score: int


# Задание 26: передаём класс и bool, а не строки.
def corrected_parse(client, prompt):
    return client.chat_parse(prompt, response_format=Result, strict=True)
