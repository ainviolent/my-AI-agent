from pathlib import Path

corpus_dir = Path(__file__).resolve().parent / 'corpus'
# Задания 22–25.
files = list(corpus_dir.glob('*.txt'))
for file_path in files:
    text = file_path.read_text(encoding='utf-8')
    document = {'source': file_path.name, 'text': text}
    clean_lines = []
    for line in text.splitlines():
        if line.strip():
            clean_lines.append(line.strip())
    clean_text = '\n'.join(clean_lines)
    print(document['source'], len(clean_text))
