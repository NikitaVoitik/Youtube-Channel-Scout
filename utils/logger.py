from loguru import logger
from pathlib import Path

root = Path.cwd()

logger.add(root / 'logs' / 'mail' / 'app.log', rotation='1 day')
logger.add(root / 'logs' / 'database' / 'app.log', rotation='1 day',
           filter=lambda record: any(file_name in record['file'].name for file_name in ['gmail.py']))
print(f'logger: {Path.cwd()}')


def get_logger():
    return logger
