import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'мой проект'))
from retrieval import MODEL_NAME, cosine_similarity, Search, load_model


def main():
    print('Задания 1–7: готовые векторы')
    vector = [0.1, 0.2, 0.3, 0.4, 0.5]
    a, b, c = [1.0, 0.0, 0.0], [0.9, 0.1, 0.0], [0.0, 0.0, 1.0]
    print('Вектор:', vector, 'Длина:', len(vector), 'Крайние:', vector[0], vector[-1])
    print('A/B:', cosine_similarity(a, b), 'A/C:', cosine_similarity(a, c), 'A/A:', cosine_similarity(a, a))
    model = load_model()
    print('Задания 8–10:')
    embedding = model.encode('Python — язык программирования')
    print('Размерность:', len(embedding), 'Первые 10 чисел:', embedding[:10].tolist())
    print('Задания 11–13: сравнение текстов')
    texts = ['Как создать список в Python?', 'Как работают списки Python?', 'Какая сегодня погода?']
    vectors = model.encode(texts)
    matrix = model.similarity(vectors, vectors).tolist()
    print('Матрица:', matrix)
    print('Близкая пара:', matrix[0][1], 'Посторонний текст:', matrix[0][2])
    print('Задания 14–21 и 30: шесть чанков по трём темам')
    chunks = [
        {'source': 'python.txt', 'chunk_id': 0, 'text': 'Список Python создаётся квадратными скобками.'},
        {'source': 'python.txt', 'chunk_id': 1, 'text': 'Цикл for повторяет действия.'},
        {'source': 'git.txt', 'chunk_id': 0, 'text': 'git commit сохраняет изменения в истории.'},
        {'source': 'git.txt', 'chunk_id': 1, 'text': 'git status показывает состояние файлов.'},
        {'source': 'pandas.txt', 'chunk_id': 0, 'text': 'DataFrame хранит табличные данные.'},
        {'source': 'pandas.txt', 'chunk_id': 1, 'text': 'read_csv читает CSV-таблицу.'}
    ]
    texts = []
    for chunk in chunks:
        texts.append(chunk['text'])
    vectors = model.encode(texts)
    for number, chunk in enumerate(chunks):
        chunk['embedding'] = vectors[number].tolist()
    question = 'Как сохранить изменения в Git?'
    query_vector = model.encode(question)
    scores = model.similarity(query_vector, vectors)[0].tolist()
    best_score = max(scores)
    best_index = scores.index(best_score)
    print('Вопрос:', question, 'Scores:', scores, 'Индекс:', best_index)
    print('Лучший:', chunks[best_index]['source'], chunks[best_index]['chunk_id'], chunks[best_index]['text'], round(best_score, 4))
    print('Поля:', list(chunks[0].keys()))
    print('Задания 22–25 и 31–32: поиск по корпусу')
    search = Search(model=model)
    questions = ['Как создать список в Python?', 'Для чего нужен return?', 'Как обработать ValueError?', 'Как вывести числа от 1 до 5?', 'Что возвращает input()?']
    for question in questions:
        print('\nВопрос:', question)
        for result in search.find(question):
            print(result['source'], result['chunk_id'], result['text'], round(result['score'], 4))
    print('Исправления 26–29: model.encode(text); best_index = scores.index(max(scores)); одна модель для всех векторов; chunks[0]["source"]')
    print('Предсказания:', 3, 1, 'b.txt')


if __name__ == '__main__':
    main()
