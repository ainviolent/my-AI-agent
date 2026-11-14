import csv
from pathlib import Path

FOLDER = Path(__file__).resolve().parent


def clean_line(line):
    line = line.replace('\u00a0', ' ').replace('\t', ' ')
    return ' '.join(line.split())


def normalize_text(text):
    lines = []
    for line in text.splitlines():
        line = clean_line(line)
        if not line or line.lower() in ['черновик', 'служебная копия']:
            continue
        if line not in lines:
            lines.append(line)
    return '\n'.join(lines)


def normalize(source=FOLDER.parent / '16 Корпус' / 'cleaned', target=FOLDER / 'normalized'):
    target.mkdir(parents=True, exist_ok=True)
    rows = []
    before_total = 0
    after_total = 0
    for path in sorted(source.glob('*.txt')):
        text = path.read_text(encoding='utf-8')
        clean = normalize_text(text)
        before = len(text)
        after = len(clean)
        percent = (before - after) / before * 100 if before else 0
        if not clean:
            print('Предупреждение: пустой результат', path.name)
            continue
        if after < 50:
            print('Предупреждение: короткий результат', path.name)
        (target / path.name).write_text(clean, encoding='utf-8')
        rows.append([path.name, before, after, round(percent, 2)])
        before_total += before
        after_total += after
        print(path.name, before, '→', after)
    with (target.parent / 'normalization_summary.csv').open('w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['source', 'before', 'after', 'reduction_percent'])
        writer.writerows(rows)
    print('Всего до:', before_total, 'После:', after_total)
    if before_total:
        print('Сокращение:', round((before_total - after_total) / before_total * 100, 2), '%')
    return rows


if __name__ == '__main__':
    normalize()
