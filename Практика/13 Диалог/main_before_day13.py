import sys
from pathlib import Path
from prompts import SYSTEM_PROMPT
from gigachat.models import Chat, Messages

sys.path.append(str(Path(__file__).resolve().parents[2] / "мой проект"))
from config import make_client

history_path = Path(__file__).with_name("chat_history.txt")
system_message = Messages(role="system", content=SYSTEM_PROMPT)
messages = [system_message]
max_pairs = 3
success_count = 0

with history_path.open("a", encoding="utf-8") as file:
    file.write("Новый запуск\n\n")

print("Команды: выход, очистить, история")

with make_client() as client:
    while True:
        question = input("Что вы хотите узнать о python? ").strip()
        command = question.lower()
        if command == "выход":
            print("Успешных обменов:", success_count)
            print("Работа завершена.")
            break
        if command == "очистить":
            messages = [system_message]
            with history_path.open("a", encoding="utf-8") as file:
                file.write("История текущего диалога очищена\n\n")
            print("История очищена. Сообщений:", len(messages))
            continue
        if command == "история":
            print("Сообщений:", len(messages))
            for message in messages:
                print(message.role)
            continue
        if not question:
            print("Введите текст.")
            continue
        messages.append(Messages(role="user", content=question))
        response = client.chat(Chat(messages=messages))
        answer = response.choices[0].message.content
        print("Ответ:")
        print(answer)
        messages.append(Messages(role="assistant", content=answer))
        success_count += 1
        if len(messages) > 1 + 2 * max_pairs:
            messages = [system_message] + messages[-2 * max_pairs:]
        print("Сообщений в истории:", len(messages))
        with history_path.open("a", encoding="utf-8") as file:
            file.write("Вы: " + question + "\n")
            file.write("Помощник: " + answer + "\n\n")
