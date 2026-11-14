# Задания 26–29. Вызывается с той же моделью, которой кодировали корпус.
def corrected_search(model, text, chunks):
    embedding = model.encode(text)
    texts = []
    for chunk in chunks:
        texts.append(chunk['text'])
    vectors = model.encode(texts)
    scores = model.similarity(embedding, vectors)[0].tolist()
    best_score = max(scores)
    best_index = scores.index(best_score)
    print(chunks[best_index]['source'])
    return chunks[best_index]
