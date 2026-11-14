import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from gigachat import GigaChat

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / '.env')


def setup_logging(folder=ROOT):
    logging.basicConfig(filename=folder / 'app.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8')
    # HTTP-журнал не должен содержать заголовки авторизации.
    logging.getLogger('httpx').setLevel(logging.WARNING)


def make_client():
    key = os.getenv('GIGACHAT_CREDENTIALS', '').strip()
    if not key:
        raise ValueError('Не задан GIGACHAT_CREDENTIALS в файле .env рядом с main.py')
    certificate = os.getenv('GIGACHAT_CA_BUNDLE_FILE')
    if not certificate:
        certificate = str(ROOT / 'certs' / 'russian_trusted_root_ca_pem.crt')
    scope = os.getenv('GIGACHAT_SCOPE', 'GIGACHAT_API_PERS')
    model = os.getenv('GIGACHAT_MODEL', 'GigaChat-2')
    return GigaChat(
        credentials=key,
        scope=scope,
        model=model,
        ca_bundle_file=certificate,
        timeout=60
    )


def log_error(error):
    # Не записываем str(error): сетевое исключение может содержать секретные данные.
    logging.error('Ошибка: %s; HTTP-статус: %s', type(error).__name__,
                  getattr(error, 'status_code', 'не указан'))

