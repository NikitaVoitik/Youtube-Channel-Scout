import asyncio
import random
from src.scraper.playwright_core import PlwCore

from utils.logger import get_logger

logger = get_logger()


class Gmail(PlwCore):
    def __init__(self, creds: dict, selectors: dict):
        super().__init__()
        self._SELECTORS: dict = selectors
        self.__creds: dict = creds

    async def check_login(self):
        compose_button = await self._page.query_selector(self._SELECTORS['compose'])
        return compose_button is not None

    async def login(self):
        logger.info('Logging in Gmail...')
        await self._bg_delay()
        sign_in_button = await self._page.query_selector(self._SELECTORS['sign_in'])
        if sign_in_button is not None:
            await self._move_and_click(sign_in_button)

        email_input = await self._page.wait_for_selector(self._SELECTORS['login'])
        await self._move_and_type(email_input, self.__creds['gmail_user'])

        password_button = await self._page.wait_for_selector(self._SELECTORS['next'])
        await self._move_and_click(password_button)

        password_input = await self._page.wait_for_selector(self._SELECTORS['password'])
        await self._move_and_type(password_input, self.__creds['gmail_pass'])
        password_button = await self._page.wait_for_selector(self._SELECTORS['next'])
        await self._move_and_click(password_button)

        logger.success('Logged in Gmail')

    async def initialise(self):
        logger.info('Initialising Gmail...')
        await super().initialise()
        await self._page.goto("https://mail.google.com/mail/u/0/?pli=1")
        await self._bg_delay()
        logger.success('Gmail initialised')

        check_login = await self.check_login()
        if not check_login:
            await self.login()

    async def sent_email(self, recipient: str, subject: str, message: str, name: str = ""):
        logger.info(f'Sending email to {recipient} by Gmail')
        compose_button = await self._page.query_selector(self._SELECTORS['compose'])
        await self._move_and_click(compose_button)

        recipient_input = await self._page.wait_for_selector(self._SELECTORS['recipient'])
        await self._move_and_type(recipient_input, recipient)
        await self._sm_delay()
        await self._page.keyboard.press('Enter')
        await self._bg_delay()

        subject_input = await self._page.wait_for_selector(self._SELECTORS['subject'])
        await self._move_and_type(subject_input, subject, allow_paste=False)

        message_input = await self._page.wait_for_selector(self._SELECTORS['message'])

        message = message.replace('{name}', f'{name}')
        await self._move_and_type(message_input, message)
        await self._bg_delay()

        send_button = await self._page.wait_for_selector(self._SELECTORS['send'])
        await self._move_and_click(send_button)
        logger.success(f'Sent email to {recipient} by Gmail')
