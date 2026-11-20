# Объяснение Python

Консольный учебный помощник на Python. Он ищет материалы по теме вопроса, передаёт найденные фрагменты в GigaChat и выводит объяснение, пример и тренировочное задание. Для обычного ответа агент использует `GigaChat-2` от Сбера, а для поиска — модель `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.

Нужен Python 3.12, интернет для первой загрузки модели MiniLM и доступ к API GigaChat для генерации. Команды ниже выполняются из `УП01/AI-Agent`.

## Установка в Ubuntu

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m pip check
if [ ! -e .env ]; then cp .env.example .env; fi
```

## Установка в Windows

Команды для PowerShell с установленным Python 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

## Настройки и запуск

В локальном `.env` укажите значение `GIGACHAT_CREDENTIALS` из своего кабинета GigaChat API и `GIGACHAT_SCOPE`, который соответствует вашему доступу. Для личного доступа обычно используется `GIGACHAT_API_PERS`. Если строка `GIGACHAT_MODEL` есть в `.env`, укажите `GigaChat-2`. Код использует модель по умолчанию, когда переменная отсутствует. `GIGACHAT_CA_BUNDLE_FILE` можно оставить пустой при наличии файла `certs/russian_trusted_root_ca_pem.crt`. Если сертификат требуется восстановить, загрузите корневой сертификат через официальную документацию GigaChat и задайте путь к локальной копии. Индекс `index.json` уже лежит рядом с `main.py`.

Ubuntu:

```bash
./.venv/bin/python main.py
```

Windows:

```powershell
.\.venv\Scripts\python.exe main.py
```

Попробуйте ввести «Что такое список в Python?» или «Как работает цикл for в Python?». Команда `история` показывает роли сообщений, `очистить` сбрасывает контекст текущего диалога, `выход` завершает программу. При пустом вводе программа просит ввести запрос. Просьба проверить код без фрагмента вызывает уточнение.

## Запуск с готовым кэшем MiniLM

Если MiniLM уже скачана, можно указать папку кэша Hugging Face и отключить запросы к Hugging Face. Например, в учебной ВМ с сохранённым проектом третьего дня:

```bash
export HF_HOME="$HOME/AI-Practice/УП01/AI-Agent/.cache/huggingface"
export HF_HUB_OFFLINE=1
./.venv/bin/python main.py
```

Если модели в кэше нет, для первой загрузки нужен интернет. Без ключа GigaChat можно проверить запуск, пустой ввод, выход и сообщение об ошибке. Чтобы проверить ответы, укажите действующий ключ и тип доступа в локальном `.env`.

## Ограничения

Точность ответа зависит от содержимого справочника. Агент подбирает до трёх фрагментов и передаёт три последние пары сообщений. Запрос к API включает текст вопроса и учебные материалы. Для ввода используйте учебные примеры без паролей и личных данных. `chat_history.txt`, `app.log`, `.env` и кэш модели храните локально. Команды Windows подготовлены по структуре проекта, фактическая проверка проводится в Ubuntu.
