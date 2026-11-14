from pathlib import Path
import csv

FOLDER = Path(__file__).resolve().parent


def clean_text(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return '\n'.join(lines)


def prepare(source=FOLDER / 'corpus', target=FOLDER / 'cleaned'):
    target.mkdir(parents=True, exist_ok=True)
    documents = []
    for path in sorted(source.glob('*.txt')):
        text = clean_text(path.read_text(encoding='utf-8'))
        if not text:
            print('Пропущен пустой файл:', path.name)
            continue
        if len(text) < 50:
            print('Предупреждение: короткий документ', path.name)
        document = {'source': path.name, 'text': text, 'category': 'Python'}
        documents.append(document)
        (target / path.name).write_text(text, encoding='utf-8')
        print(path.name, len(text), 'символов')
    total = sum(len(document['text']) for document in documents)
    print('Документов:', len(documents), 'Всего символов:', total)
    if documents:
        print('Самый длинный:', max(documents, key=lambda d: len(d['text']))['source'])
        print('Самый короткий:', min(documents, key=lambda d: len(d['text']))['source'])
        print('Средняя длина:', round(total / len(documents), 1))
    with (target.parent / 'corpus_summary.csv').open('w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['source', 'category', 'length'])
        for document in documents:
            writer.writerow([document['source'], document['category'], len(document['text'])])
    return documents


if __name__ == '__main__':
    prepare()
