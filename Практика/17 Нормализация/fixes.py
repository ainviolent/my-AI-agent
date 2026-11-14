from pathlib import Path

# Задания 25–28.
text = '  Python\t  язык  '
words = text.split()
clean = ' '.join(words)
print(clean)
text = text.replace('\t', ' ')


def clean_line(line):
    line = ' '.join(line.split())
    return line


normalized_dir = Path(__file__).resolve().parent / 'normalized'
normalized_dir.mkdir(exist_ok=True)
