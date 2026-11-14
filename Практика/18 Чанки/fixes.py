from pathlib import Path

text = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
chunk_size = 10
# Задание 26: шаг равен размеру чанка.
chunks = []
for start in range(0, len(text), chunk_size):
    chunk = text[start:start + chunk_size]
    chunks.append(chunk)
# Задание 27: правильный порядок вычитания.
overlap = 2
step = chunk_size - overlap
# Задание 28: распаковка номера и текста.
for chunk_id, chunk in enumerate(chunks):
    print(chunk_id, chunk)
# Задание 29: число преобразуется внутри f-строки.
file_path = Path('python.txt')
filename = f'{file_path.stem}_chunk_{chunk_id}.txt'
print(filename)
