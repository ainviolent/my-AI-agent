import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault('HF_HOME', str(ROOT / '.cache' / 'huggingface'))
MODEL_NAME = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'


def cosine_similarity(first, second):
    from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine
    return float(sklearn_cosine([first], [second])[0][0])


def load_model():
    from sentence_transformers import SentenceTransformer
    local = ROOT / '.cache' / 'local_model'
    if (local / 'model.safetensors').exists():
        return SentenceTransformer(str(local))
    return SentenceTransformer(MODEL_NAME)


def build_index(chunks_path, output_path):
    chunks = []
    text = Path(chunks_path).read_text(encoding='utf-8')
    for line in text.splitlines():
        if line.strip():
            chunks.append(json.loads(line))
    if not chunks:
        raise ValueError('Нет чанков. Сначала выполните дни 16–18.')
    model = load_model()
    texts = []
    for chunk in chunks:
        texts.append(chunk['text'])
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    for number in range(len(chunks)):
        chunks[number]['embedding'] = vectors[number].tolist()
    data = {'model': MODEL_NAME, 'chunks': chunks}
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    return model


class Search:
    def __init__(self, index_path=ROOT / 'index.json', model=None):
        data = json.loads(Path(index_path).read_text(encoding='utf-8'))
        if data['model'] != MODEL_NAME:
            raise ValueError('Индекс создан другой моделью. Пересоздайте его.')
        self.chunks = data['chunks']
        if not self.chunks:
            raise ValueError('Индекс пуст')
        if model is None:
            self.model = load_model()
        else:
            self.model = model

    def find(self, question, top_k=3, threshold=0.35):
        if not question.strip():
            return []
        vector = self.model.encode(question, show_progress_bar=False)
        embeddings = []
        for chunk in self.chunks:
            embeddings.append(chunk['embedding'])
        scores = self.model.similarity(vector, embeddings)[0].tolist()
        results = []
        for number, chunk in enumerate(self.chunks):
            score = scores[number]
            if score >= threshold:
                result = {'source': chunk['source'], 'chunk_id': chunk['chunk_id'],
                          'text': chunk['text'], 'score': score}
                results.append(result)
        results.sort(key=lambda item: item['score'], reverse=True)
        return results[:top_k]

