import logging
import sys
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parents[1] / 'мой проект'))
from config import make_client, setup_logging, log_error


class Book(BaseModel):
    title: str = Field(description='Название книги')
    author: str = Field(description='Автор')
    year: int = Field(description='Год издания')


class StudentInfo(BaseModel):
    name: str = Field(description='Имя студента')
    group: str = Field(description='Группа')
    score: int = Field(description='Балл')


class Classification(BaseModel):
    category: str = Field(description='Категория сообщения')
    confidence: int = Field(description='Уверенность от 0 до 100')


class TopicAnalysis(BaseModel):
    topic: str = Field(description='Тема вопроса')
    difficulty: str = Field(description='Сложность вопроса')
    summary: str = Field(description='Краткое объяснение')


class Appeal(BaseModel):
    category: str = Field(description='Категория обращения')
    priority: str = Field(description='Приоритет')
    summary: str = Field(description='Содержание обращения')


def main():
    setup_logging(FOLDER)
    book = Book(title='Учебник Python', author='Учебный пример', year=2026)
    print(book.model_dump())
    try:
        Book(title='Пример', author='Студент', year='не число')
    except ValidationError:
        print('Pydantic обнаружил неверный тип года')
    schemas = {'студент': StudentInfo, 'класс': Classification, 'тема': TopicAnalysis, 'обращение': Appeal}
    mode = input('Режим (студент, класс, тема, обращение): ').strip()
    text = input('Введите текст: ').strip()
    if not text or mode not in schemas:
        print('Проверьте режим и текст')
        logging.warning('Пустой ввод или неизвестный режим')
        return
    try:
        logging.info('Отправка запроса')
        with make_client() as client:
            completion, parsed = client.chat_parse('Заполни поля по тексту: ' + text,
                                                   response_format=schemas[mode], strict=True)
        for field, value in parsed.model_dump().items():
            print(field, value)
        logging.info('Ответ получен')
    except Exception as error:
        log_error(error)
        print('Не удалось получить ответ')


if __name__ == '__main__':
    main()
