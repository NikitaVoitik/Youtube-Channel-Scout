import json
from pathlib import Path
import os

root = Path.cwd()

def load_config() -> dict:
    with open(root / 'config.json', 'r') as f:
        config = json.load(f)
    return config


def load_json(path: str) -> dict:
    with open(root / 'data' / f'{path}', 'r') as f:
        js = json.load(f)
    return js


def load_queries() -> [str]:
    with open(root / 'data' / 'queries.txt', 'r') as f:
        queries = [x[:-1] for x in f.readlines()]
    return queries

CONFIG = load_config()
MAIL_CREDS = {
    'gmail_user': os.getenv('EMAIL_USER'),
    'gmail_pass': os.getenv('EMAIL_PASS')
}
SELECTORS = load_json('selectors.json')
