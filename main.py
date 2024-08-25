import asyncio
import random
from src.scraper.gmail import Gmail
from utils.data import MAIL_CREDS, SELECTORS, SUBJECTS, TEXTS
import sys
from utils.logger import get_logger

logger = get_logger()


async def task():
    for ind in range(10000):
        print(f'op: {ind}')
        await asyncio.sleep(1)


async def ainput() -> str:
    return (await asyncio.to_thread(sys.stdin.readline)).rstrip('\n')


async def start_gmail() -> Gmail:
    creds = {key: MAIL_CREDS[key] for key in ['gmail_user', 'gmail_pass']}
    gmail = Gmail(creds, SELECTORS.get('gmail'))
    await gmail.initialise()
    return gmail


async def main():
    logger.success('Application started')
    gmail = await start_gmail()
    while True:
        email_data = await ainput()
        if ":" in email_data:
            email_data = email_data.split(":")
        else:
            email_data = [email_data, ""]
        await gmail.sent_email(
            email_data[0],
            random.choice(SUBJECTS),
            random.choice(TEXTS),
            email_data[1]
        )
        await asyncio.sleep(random.randint(15, 30) * 60)


if __name__ == '__main__':
    asyncio.run(main())
