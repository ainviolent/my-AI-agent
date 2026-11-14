import logging
import sys
from pathlib import Path
from pydantic import BaseModel, Field

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parents[1] / 'мой проект'))
from config import make_client, setup_logging, log_error


class AnalysisResult(BaseModel):
    topic: str = Field(description='Тема вопроса')
    category: str = Field(description='Категория: Python или другая тема')
    difficulty: str = Field(description='Сложность: низкая, средняя или высокая')
    summary: str = Field(description='Краткое понятное объяснение')


def analyze(text):
    text = text.strip()
    if not text:
        logging.warning('Пустой ввод')
        print('Введите учебный вопрос')
        return None
    try:
        logging.info('Подготовлен запрос анализа')
        prompt = 'Проанализируй учебный вопрос. Ответь по-русски простыми словами: ' + text
        with make_client() as client:
            completion, parsed = client.chat_parse(prompt, response_format=AnalysisResult, strict=True)
        for name, value in parsed.model_dump().items():
            print(name + ':', value)
        logging.info('Структурированный ответ получен и проверен')
        (FOLDER / 'result.txt').write_text(parsed.model_dump_json(indent=2), encoding='utf-8')
        return parsed
    except Exception as error:
        log_error(error)
        print('Не удалось получить ответ')
        return None


if __name__ == '__main__':
    setup_logging(FOLDER)
    logging.info('Программа запущена')
    analyze(input('Введите учебный вопрос: '))
