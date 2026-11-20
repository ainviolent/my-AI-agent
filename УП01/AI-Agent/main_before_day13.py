import logging
import os
from dotenv import load_dotenv
from gigachat import GigaChat
from pydantic import BaseModel, Field
from gigachat.models import Chat, Messages
from config import ROOT, setup_logging, log_error
from prompts import SYSTEM_PROMPT
from retrieval import Search

load_dotenv(ROOT / ".env")
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")

EMPTY = 'Введите вопрос о Python.'
NOT_FOUND = 'В базе знаний нет подходящего ответа. Уточните вопрос о Python.'


class LessonAnswer(BaseModel):
    topic: str = Field(description='Тема вопроса по Python')
    explanation: str = Field(description='Короткое объяснение по материалам или один уточняющий вопрос')
    example: str = Field(description='Короткий пример кода. Если нужно уточнение, верни пустую строку')
    exercise: str = Field(description='Одно задание без решения. Если нужно уточнение, верни пустую строку')


def missing_code(question, history):
    text = question.lower().replace('ё', 'е')
    requests = ['проверь код', 'проверь мой код', 'посмотри мой код',
                'посмотреть мой код', 'разбери мой код', 'исправь мой код',
                'проверь мое решение', 'найди ошибку в моем коде']

    check_code = False
    for phrase in requests:
        if phrase in text:
            check_code = True
            break
    if not check_code:
        return False

    messages = [question]
    for message in history:
        if message['role'] == 'user':
            messages.append(message['content'])

    marks = ['`', '=', '[', '{', 'print(', 'import ', 'def ',
             ' in ', 'return ', 'if ', 'while ']
    for message in messages:
        for mark in marks:
            if mark in message:
                return False
        if '(' in message and ')' in message:
            if '?' not in message or ':' in message:
                return False
    return True


def main():
    setup_logging()
    logging.info("Запуск программы")
    try:
        search = Search()
        with (ROOT / "chat_history.txt").open("a", encoding="utf-8") as file:
            file.write("Новый запуск\n\n")
    except Exception as error:
        log_error(error)
        print("Не удалось подготовить поиск или открыть файл истории.")
        return

    system_message = {"role": "system", "content": SYSTEM_PROMPT}
    messages = [system_message]
    max_pairs = 3
    success_count = 0
    print("Команды: выход, очистить, история")

    while True:
        try:
            question = input("Что вы хотите узнать о Python? ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nРабота завершена.")
            break

        command = question.lower()
        if command == "выход":
            print("Успешных обменов:", success_count)
            print("Работа завершена.")
            break
        if command == "очистить":
            try:
                with (ROOT / "chat_history.txt").open("a", encoding="utf-8") as file:
                    file.write("История текущего диалога очищена\n\n")
            except Exception as error:
                log_error(error)
                print("Не удалось записать событие очистки в файл.")
            messages = [system_message]
            print("История очищена. Сообщений:", len(messages))
            continue
        if command == "история":
            print("Сообщений:", len(messages))
            for message in messages:
                print(message["role"])
            continue
        if not question:
            print("Введите запрос")
            logging.warning("Пустой ввод")
            continue
        if missing_code(question, messages[1:]):
            print("Пришли свой фрагмент кода и текст ошибки, если он есть.")
            continue

        search_question = question
        if len(messages) > 1:
            for word in ["это", "этот", "второ", "подробнее"]:
                if word in question.lower():
                    search_question = messages[-2]["content"] + "\n" + question
                    break

        try:
            results = search.find(search_question)
            if not results:
                print(NOT_FOUND)
                logging.warning("Подходящий контекст не найден")
                continue

            context = ""
            sources = []
            for result in results:
                context += "\nИсточник: " + result["source"] + "\n" + result["text"] + "\n"
                if result["source"] not in sources:
                    sources.append(result["source"])

            instructions = SYSTEM_PROMPT + "\n\nМатериалы учебного справочника:\n" + context
            request_messages = [Messages(role="system", content=instructions)]
            for message in messages[1:]:
                request_messages.append(Messages(role=message["role"], content=message["content"]))
            request_messages.append(Messages(role="user", content=question))

            logging.info("Контекст найден, запрос отправляется")
            if not key:
                raise ValueError("Не задан GIGACHAT_CREDENTIALS в .env")
            certificate = os.getenv("GIGACHAT_CA_BUNDLE_FILE")
            if not certificate:
                certificate = str(ROOT / "certs" / "russian_trusted_root_ca_pem.crt")
            with GigaChat(
                credentials=key,
                scope=scope,
                model=os.getenv("GIGACHAT_MODEL", "GigaChat-2"),
                ca_bundle_file=certificate,
                timeout=60
            ) as client:
                completion, parsed = client.chat_parse(
                    Chat(messages=request_messages),
                    response_format=LessonAnswer,
                    strict=True
                )
            if not parsed.explanation.strip():
                raise ValueError("Пустой ответ API")

            answer = "Тема: " + parsed.topic + "\n" + parsed.explanation
            if parsed.example.strip():
                answer += "\n\nПример:\n" + parsed.example
            if parsed.exercise.strip():
                answer += "\n\nЗадание:\n" + parsed.exercise
            answer += "\n\nИсточники найденных материалов: " + ", ".join(sources)
        except Exception as error:
            log_error(error)
            print("Не удалось получить ответ. Проверьте ключ, доступ к API и подключение.")
            continue

        print("Ответ:")
        print(answer)
        messages.append({"role": "user", "content": question})
        messages.append({"role": "assistant", "content": answer})
        success_count += 1
        while len(messages) > 1 + 2 * max_pairs:
            messages.pop(1)
        print("Сообщений в истории:", len(messages))

        try:
            with (ROOT / "chat_history.txt").open("a", encoding="utf-8") as file:
                file.write("Вы: " + question + "\n")
                file.write("Помощник: " + answer + "\n\n")
        except Exception as error:
            log_error(error)
            print("Не удалось сохранить этот диалог в файл.")
        logging.info("Ответ получен и выведен")


if __name__ == "__main__":
    main()
