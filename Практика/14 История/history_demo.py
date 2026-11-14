# Четыре обмена без обращения к API. Системное сообщение плюс три последние пары.
messages = [{'role': 'system', 'content': 'Помощник по Python'}]
max_pairs = 3
for number in range(1, 5):
    messages.append({'role': 'user', 'content': 'Вопрос ' + str(number)})
    messages.append({'role': 'assistant', 'content': 'Ответ ' + str(number)})
    messages = messages[:1] + messages[-2 * max_pairs:] if len(messages) > 7 else messages
print('Сообщений:', len(messages))
for message in messages:
    print(message['role'], message['content'])
