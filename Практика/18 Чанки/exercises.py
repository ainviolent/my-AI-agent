from pathlib import Path
from final_day18 import split_into_chunks, split_with_overlap, chunk_corpus, FOLDER


def main():
    text = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234'
    print('Задания 1–4:', split_into_chunks(text, 10), split_into_chunks(text, 7))
    print('Задание 5. Шаг:', 100 - 20)
    print('Задания 6–7:', split_with_overlap(text, 20, 5, 1))
    print('Задание 8. Неверный overlap:')
    try:
        split_with_overlap(text, 20, 20)
    except ValueError as error:
        print(error)
    print('Задания 9–11. Пустые/короткие:', split_with_overlap('   ', 20, 5, 1), split_with_overlap('короткий', 20, 5, 20))
    path = sorted((FOLDER.parent / '17 Нормализация' / 'normalized').glob('*.txt'))[0]
    document = path.read_text(encoding='utf-8')
    print('Задания 12–18. Три соседних чанка:')
    for chunk_id, part in enumerate(split_with_overlap(document, 200, 40)[:3]):
        print({'source': path.name, 'chunk_id': chunk_id, 'length': len(part), 'text': part})
    print('Задания 19–25, 31–32. Все документы:')
    chunk_corpus()
    print('Исправления 26–29: range(0, len(text), chunk_size); step = chunk_size - overlap; for chunk_id, chunk in enumerate(chunks); f"{path.stem}_chunk_{chunk_id}.txt"')
    print('Предсказания:', 'ABCDEFGHIJ'[0:4], 10 - 3, list(enumerate(['A', 'B', 'C'])))
    print('Задание 30 и звёздочка. Чанков одного документа:')
    for size, overlap in [(200, 40), (400, 80)]:
        count = len(split_with_overlap(document, size, overlap))
        print('Размер:', size, 'Перекрытие:', overlap, 'Количество:', count)


if __name__ == '__main__':
    main()
