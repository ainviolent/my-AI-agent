from pathlib import Path
from tempfile import TemporaryDirectory
from final_day16 import clean_text, prepare, FOLDER


def main():
    print('Задания 1–9: тематический корпус, glob, чтение и словари')
    paths = sorted((FOLDER / 'corpus').glob('*.txt'))
    print('Найдено:', len(paths))
    texts = []
    documents = []
    for path in paths:
        text = path.read_text(encoding='utf-8')
        texts.append(text)
        documents.append({'source': path.name, 'text': text})
        print(path.name, 'строк:', len(text.splitlines()))
    print('Первый документ:', documents[0])
    print('Задания 10–18: пустой и короткий файлы проверяются отдельно от итогового корпуса')
    with TemporaryDirectory() as tmp:
        source = Path(tmp) / 'corpus'
        source.mkdir()
        (source / 'empty.txt').write_text('   \n', encoding='utf-8')
        (source / 'short.txt').write_text('  Python  \n\n  print()  ', encoding='utf-8')
        prepare(source, Path(tmp) / 'cleaned')
        print('До:   Python  / пустая строка /   print()')
        print('После:', (Path(tmp) / 'cleaned' / 'short.txt').read_text())
    print('Задания 19–21, 26–29: Python — выбранная тема, сводка и крайние длины')
    prepare()
    print('Исправления 22–25: glob("*.txt"), read_text(encoding="utf-8"), двоеточие в словаре, join(lines)')
    print('Предсказания:', '  Python  '.strip(), len(['A', '', 'B']), [{'source': 'a.txt', 'text': 'ABC'}][0]['source'])


if __name__ == '__main__':
    main()
