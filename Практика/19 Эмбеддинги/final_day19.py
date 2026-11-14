import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'мой проект'))
from retrieval import Search, build_index


def main():
    chunks = ROOT / 'Практика' / '18 Чанки' / 'chunks.jsonl'
    index = ROOT / 'мой проект' / 'index.json'
    model = build_index(chunks, index)
    search = Search(index, model=model)
    print('Введите минимум три вопроса. Команда завершения: выход')
    while True:
        try:
            question = input('Вопрос: ').strip()
        except (EOFError, KeyboardInterrupt):
            break
        if question.lower() == 'выход':
            break
        if not question:
            print('Введите текст вопроса')
            continue
        results = search.find(question)
        if not results:
            print('Подходящий фрагмент не найден')
        for result in results:
            print('Источник:', result['source'])
            print('Чанк:', result['chunk_id'])
            print('Текст:', result['text'])
            print('Сходство:', round(result['score'], 4))


if __name__ == '__main__':
    main()
