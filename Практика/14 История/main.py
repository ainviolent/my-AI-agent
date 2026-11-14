import sys
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'мой проект'))
from gigachat.models import Chat, Messages
from config import make_client, setup_logging, log_error

SYSTEM = 'Ты — помощник начинающего изучать Python. Объясняй просто, покажи пример и предложи задание без решения.'


def main():
    setup_logging(Path(__file__).resolve().parent)
    history = []
    success_count = 0
    print('Команды: выход, история, очистить')
    while True:
        try:
            question = input('Вопрос о Python: ').strip()
        except (EOFError, KeyboardInterrupt):
            break
        command = question.lower()
        if command == 'выход':
            print('Успешных обменов:', success_count)
            break
        if command == 'история':
            print('Сообщений:', 1 + len(history))
            print('system')
            for message in history:
                print(message.role.value)
            continue
        if command == 'очистить':
            history.clear()
            print('История очищена. Сообщений: 1')
            continue
        if not question:
            print('Введите текст.')
            continue
        messages = [Messages(role='system', content=SYSTEM)] + history
        messages.append(Messages(role='user', content=question))
        try:
            with make_client() as client:
                response = client.chat(Chat(messages=messages))
            answer = response.choices[0].message.content
        except Exception as error:
            log_error(error)
            print('Не удалось получить ответ')
            continue
        print(answer)
        history.extend([Messages(role='user', content=question), Messages(role='assistant', content=answer)])
        history = history[-6:]
        success_count += 1
        with (Path(__file__).resolve().parent / 'chat_history.txt').open('a', encoding='utf-8') as file:
            file.write('Вы: ' + question + '\nПомощник: ' + answer + '\n\n')


if __name__ == '__main__':
    main()
