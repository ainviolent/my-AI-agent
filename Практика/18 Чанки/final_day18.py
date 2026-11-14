import csv
import json
from pathlib import Path

FOLDER = Path(__file__).resolve().parent


def split_into_chunks(text, chunk_size):
    return split_with_overlap(text, chunk_size, 0, 1)


def split_with_overlap(text, chunk_size, overlap, minimum_length=30):
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError('Нужно: chunk_size > 0 и 0 <= overlap < chunk_size')
    if minimum_length < 1:
        raise ValueError('minimum_length должен быть положительным')
    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size].strip()
        if len(chunk) >= minimum_length:
            chunks.append(chunk)
        if start + chunk_size >= len(text):
            break
    return chunks


def chunk_corpus(chunk_size=400, overlap=80):
    files = sorted((FOLDER.parent / '17 Нормализация' / 'normalized').glob('*.txt'))
    target = FOLDER / 'chunks'
    target.mkdir(exist_ok=True)
    all_chunks = []
    for document_index, path in enumerate(files):
        text = path.read_text(encoding='utf-8')
        parts = split_with_overlap(text, chunk_size, overlap)
        for chunk_id, part in enumerate(parts):
            chunk = {'source': path.name, 'chunk_id': chunk_id, 'length': len(part),
                     'text': part, 'document_index': document_index}
            all_chunks.append(chunk)
            (target / f'{path.stem}_chunk_{chunk_id}.txt').write_text(part, encoding='utf-8')
    with (FOLDER / 'chunks_summary.csv').open('w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['source', 'chunk_id', 'length'])
        for chunk in all_chunks:
            writer.writerow([chunk['source'], chunk['chunk_id'], chunk['length']])
    (FOLDER / 'chunks.jsonl').write_text('\n'.join(json.dumps(c, ensure_ascii=False) for c in all_chunks), encoding='utf-8')
    print('Документов:', len(files), 'Всего чанков:', len(all_chunks))
    if all_chunks:
        print('Средняя длина:', round(sum(c['length'] for c in all_chunks) / len(all_chunks), 1))
    return all_chunks


if __name__ == '__main__':
    chunk_corpus()
