from os import getenv
from pathlib import Path

TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN', '')

TELEGRAM_BOT_CHAT = getenv('TELEGRAM_BOT_CHAT', '')
TELEGRAM_MAIN_CHANNEL = getenv('TELEGRAM_MAIN_CHANNEL', '')
TELEGRAM_VKUPDATES_CHANNEL = getenv('TELEGRAM_VKUPDATES_CHANNEL', '')

OWNER_ID = int(getenv('OWNER_ID', '0'))

VK_TOKEN = getenv('VK_TOKEN', '')
VK_GROUP_ID = getenv('VK_GROUP_ID', '')
VK_APP_ID = getenv('VK_APP_ID', '')

WEBHOOK_HOST = getenv('VK_TOKEN', '')
WEBHOOK_PORT = getenv('VK_TOKEN', '')
WEBHOOK_LISTEN = getenv('VK_TOKEN', '0.0.0.0')
# Generate it with "openssl genrsa -out webhook_pkey.pem 2048"
WEBHOOK_SSL_CERT = Path.cwd() / getenv('WEBHOOK_SSL_CERT', 'webhook_cert.pem')
# Generate it with "openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem"
WEBHOOK_SSL_PRIV = Path.cwd() / getenv('WEBHOOK_SSL_PRIV', 'webhook_pkey.pem')
WEBHOOK_URL_BASE = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}"
WEBHOOK_URL_PATH = f"/{TELEGRAM_TOKEN}/"

BANNED_TAGS = {'comic', 'loli', 'shota'}

DANBOORU_LOGIN = getenv('DANBOORU_LOGIN', '')
DANBOORU_API_KEY = getenv('DANBOORU_API_KEY', '')

GELBOORU_LOGIN = getenv('GELBOORU_LOGIN', '')
GELBOORU_PASSWORD = getenv('GELBOORU_PASSWORD', '')

PIXIV_LOGIN = getenv('PIXIV_LOGIN', '')
PIXIV_PASSWORD = getenv('PIXIV_PASSWORD', '')

DEFAULT_SERVICE = getenv('DEFAULT_SERVICE', 'dan')

IMAGES_FOLDER = Path.cwd() / getenv('IMAGES_FOLDER',  'pics')