import asyncio
import random

from proto import MESSAGE

from src.mail.gmail import Gmail
from utils.data import MAIL_CREDS, SELECTORS, SUBJECTS, TEXTS
import sys


async def task():
    for ind in range(10000):
        # print(f'op: {ind}')
        await asyncio.sleep(1)


async def ainput() -> str:
    # await asyncio.to_thread(sys.stdout.write, f'{string} ')
    return (await asyncio.to_thread(sys.stdin.readline)).rstrip('\n')


async def start_gmail() -> Gmail:
    creds = {key: MAIL_CREDS[key] for key in ['gmail_pass', 'gmail_pass']}
    gmail = Gmail(creds, SELECTORS.get('gmail'))
    await gmail.initialise()
    return gmail


async def main():
    print('start')
    gmail = await start_gmail()
    # await gmail.sent_email('nikitavoitik2006@gmail.com', 'test test test test test',
    #                       'lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore ')
    while True:
        email_data = await ainput()
        if " " in email_data:
            email_data = email_data.split(" ")
        print(email_data)
        print("" if len(email_data) == 1 else email_data[1])
        await gmail.sent_email(
            email_data[0],
            random.choice(SUBJECTS),
            random.choice(TEXTS),
            "" if len(email_data) == 1 else email_data[1]
        )
        #await asyncio.sleep(random.randint(15, 30) * 60)


if __name__ == '__main__':
    asyncio.run(main())
