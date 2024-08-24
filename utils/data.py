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


def load_txt(path) -> [str]:
    with open(root / 'data' / f'{path}', 'r') as f:
        queries = [x[:-1] for x in f.readlines()]
    return queries


def load_messages(path) -> [str]:
    messages = []
    with open(root / 'data' / f'{path}', 'r') as f:
        lines = f.readlines()
        message = ""
        for line in lines:
            if line.startswith('/end'):
                messages.append(message)
                message = ""
                continue
            message += line
    return messages


CONFIG = load_config()
MAIL_CREDS = {
    'gmail_user': os.getenv('GMAIL_USER'),
    'gmail_pass': os.getenv('GMAIL_PASS')
}
SELECTORS = load_json('selectors.json')
SUBJECTS = load_txt('emails/subject.txt')
TEXTS = load_messages('emails/text.txt')
