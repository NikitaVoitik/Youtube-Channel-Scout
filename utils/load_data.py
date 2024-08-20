import json
from pathlib import Path

root = Path.cwd()

def load_config() -> dict:
    with open(root / 'data' / 'config.json', 'r') as f:
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
