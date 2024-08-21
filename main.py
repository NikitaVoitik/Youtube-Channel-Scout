import asyncio
from src.mail.gmail import Gmail
from src.utils.data import CONFIG, MAIL_CREDS, SELECTORS


async def task():
    for ind in range(10000):
        print(f'op: {ind}')
        await asyncio.sleep(1)


async def start_gmail() -> Gmail:
    creds = {key: MAIL_CREDS[key] for key in ['gmail_pass', 'gmail_pass']}
    gmail = Gmail(creds, SELECTORS.get('gmail'))
    await gmail.initialise()
    return gmail

async def main():
    gmail = await start_gmail()
    await gmail.sent_email('nikitavoitik2006@gmail.com', 'test test test test test',
                           'lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore lorem ipsum lokrem ipsum lore ')
    # await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
