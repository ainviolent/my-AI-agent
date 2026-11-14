from pathlib import Path
from final_day17 import clean_line, normalize_text, normalize, FOLDER


def main():
    print('Задания 1–8: strip, табуляция, split, join, строки')
    dirty = '  Python\t —\u00a0   язык программирования. \n\nПеременная хранит значение.\nПеременная хранит значение.\nЧерновик\nЧерновик решения сохраняется.\n'
    print('До:', repr(dirty))
    print('После:', normalize_text(dirty))
    print('Задания 9–14: порядок и регистр')
    print(normalize_text('A\nA\nB\nPython\npython'))
    print('Python'.lower() == 'python'.lower())
    print('Задания 15–20: функция, пустой текст, измерение')
    clean = normalize_text(dirty)
    print('Пустой:', repr(normalize_text('   \n\t')))
    print('До:', len(dirty), 'После:', len(clean), 'Удалено:', len(dirty) - len(clean))
    print('Сокращение:', round((len(dirty) - len(clean)) / len(dirty) * 100, 1), '%')
    print('Задания 21–24, 30–31: весь корпус и CSV')
    normalize()
    print('Исправления 25–28: join(words), replace("\\t", " "), def clean_line(line):, mkdir(exist_ok=True)')
    print('Предсказания:', ' '.join('  A   B  '.split()), '\tPython\t'.strip(), ['A', 'B'])
    print('Задание 29: отдельная инструкция')
    (FOLDER / 'dirty_instruction.txt').write_text(dirty, encoding='utf-8')
    (FOLDER / 'clean_instruction.txt').write_text(clean, encoding='utf-8')


if __name__ == '__main__':
    main()
