import logging
from pydantic import ValidationError
from structured_output import Book, StudentInfo, Classification, TopicAnalysis, Appeal
from final_day15 import AnalysisResult, analyze, FOLDER
from config import setup_logging


def main():
    setup_logging(FOLDER)
    print('Задания 1–2. Обработка ошибки:')
    try:
        int('не число')
    except ValueError as error:
        print('Введите целое число. Тип ошибки:', type(error).__name__)
    print('Задания 3–11: api_errors.py и logging_demo.py. Три уровня журнала:')
    logging.info('Программа запущена')
    logging.warning('Учебное предупреждение')
    logging.error('Учебная ошибка без API-ключа')
    print('Задания 12–15:')
    book = Book(title='Учебник Python', author='Учебный пример', year=2026)
    print(book.title, book.author, book.year)
    try:
        Book(title='Пример', author='Автор', year='не число')
    except ValidationError as error:
        print('Ошибка проверки:', error.errors()[0]['type'])
    print('Задания 16–19, 27–29: режимы студент, класс, тема, обращение в structured_output.py')
    print('Задания 20–22, 30: final_day15.py, четыре поля и strict=True')
    print('Пустой ввод не обращается к API:')
    analyze('   ')
    print('Исправления 23–26: двоеточия try/except; запятая после filename; поля category: str; response_format=AnalysisResult, strict=True')
    print('Предсказания:', '   '.strip() == '', 'app.log', 5)


if __name__ == '__main__':
    main()
