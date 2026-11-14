import logging
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parents[1] / 'мой проект'))
from config import make_client, setup_logging, log_error
from prompts import SYSTEM_PROMPT


def main():
    setup_logging(FOLDER)
    text = input('Что вы хотите узнать о Python? ').strip()
    if not text:
        print('Введите вопрос')
        logging.warning('Пустой ввод')
        return
    try:
        logging.info('Отправка запроса')
        with make_client() as client:
            response = client.chat(SYSTEM_PROMPT + '\nВопрос: ' + text)
        print(response.choices[0].message.content)
        logging.info('Ответ получен')
    except Exception as error:
        log_error(error)
        print('Не удалось получить ответ')


if __name__ == '__main__':
    main()
