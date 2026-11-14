import logging
from pathlib import Path
logging.basicConfig(filename=Path(__file__).with_name("app.log"), level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")
logging.info("Программа запущена")
logging.warning("Учебный пример предупреждения")
logging.error("Учебный пример ошибки")
try:
    print(int(input("Введите число: ")))
except ValueError as error:
    print("Введите целое число")
    logging.error("Ошибка ввода: %s", type(error).__name__)
