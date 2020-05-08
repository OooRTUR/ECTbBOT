import os

TOKEN = os.getenv('TELEGRAM_TOKEN')

REQUEST_KWARGS={
    'proxy_url': os.getenv('PROXY_URL'),
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': os.getenv('PROXY_USERNAME'),
        'password': os.getenv('PROXY_PASS'),
    }
}

ACCESS_IDS = os.getenv('TELEGRAM_ACCESS_IDS').split('; ')