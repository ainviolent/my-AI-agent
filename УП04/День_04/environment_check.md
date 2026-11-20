# Проверка среды

20.11.2026. Агент «Объяснение Python». [Репозиторий](https://github.com/ainviolent/my-AI-agent), исходный коммит `df0c5f9`.

| Что проверил | Результат |
|---|---|
| Система и папка | Ubuntu 24.04.5 LTS в VirtualBox, `~/AI-Practice-Repo/УП01/AI-Agent` |
| Python и окружение | Python 3.12.3, новая `.venv`, pip 24.0 |
| Точка запуска | `main.py` вызывает `main()` из `main_before_day13.py` |
| Файлы | На месте `requirements.txt`, `README.md`, `.env.example`, `config.py`, `prompts.py`, `retrieval.py`, `index.json` и сертификат из `certs/` |
| Поиск | MiniLM из семейства sentence-transformers. Модель найдена в кэше третьего дня. Новый пакет весов не скачивался |
| Генерация | Внешняя модель GigaChat-2. HTTPS-запрос без ключа получил 401. Авторизованный доступ не проверен |
| Настройки | Четыре имени в `.env.example` совпадают с кодом. Рабочего ключа в тестовой среде нет |

Сверил требования с третьим днём. Поставил CPU-сборку PyTorch 2.2.2+cpu, затем пакеты из requirements.txt. Проверенные версии: gigachat 0.2.3, python-dotenv 1.2.4, pydantic 2.14.4, sentence-transformers 3.4.1, transformers 4.46.3, numpy 1.26.4 и huggingface-hub 0.36.2. pip check выдал `No broken requirements found.`
