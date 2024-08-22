from playwright.async_api import async_playwright, Page, BrowserContext, Playwright
import asyncio
import random

from python_ghost_cursor.playwright_async import create_cursor
from python_ghost_cursor.playwright_async._spoof import GhostCursor

from utils.logger import get_logger

logger = get_logger()


class Gmail:
    def __init__(self, creds, selectors):
        self.cursor: GhostCursor | None = None
        self.playwright: Playwright | None = None
        self._SELECTORS = selectors
        self.__creds = creds
        self.page: Page | None = None
        self.browser: BrowserContext | None = None

    async def _move_cursor_randomly_left(self):
        elements = await self.page.query_selector_all('body *')

        for element in elements:
            bounding_box = await element.bounding_box()
            viewport = self.page.viewport_size['width']
            if bounding_box and bounding_box['x'] < viewport / 2:
                await self.cursor.move(element)
                break

    @staticmethod
    async def _sm_delay():
        await asyncio.sleep(random.uniform(0.1, 0.4))

    @staticmethod
    async def _md_delay():
        await asyncio.sleep(random.uniform(0.5, 1.1))

    @staticmethod
    async def _bg_delay():
        await asyncio.sleep(random.uniform(1.1, 1.8))

    async def _move_and_click(self, element):
        await self._sm_delay()
        await self.cursor.click(element, wait_for_click=random.randint(200, 600))
        await self._md_delay()

    async def _move_and_type(self, element, text, allow_paste=True):
        await self._move_and_click(element)
        await self._sm_delay()
        await self._type_text(element, text, allow_paste)
        await self._md_delay()

    async def _typing_mistake(self, element):
        if random.randint(1, 100) < 5:
            wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz ')
            await element.type(wrong_char)
            await asyncio.sleep(random.uniform(0.5, 1.2))
            await self._typing_mistake(element)
            await element.press('Backspace')
            await asyncio.sleep(random.uniform(0.5, 0.15))

    async def _move_to_random_element(self):
        elements = await self.page.query_selector_all('div')
        random_element = random.choice(elements)
        await self.cursor.move_to(random_element)
        await self._md_delay()

    @staticmethod
    async def _type_text(element, text, allow_paste=True):
        if allow_paste:
            chance = random.randint(1, 100)
            if chance <= 30:
                await element.fill(text)
                print('paste')
                return
        for char in text:
            while random.randint(1, 100) < 8:
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                await element.type(wrong_char)
                await asyncio.sleep(random.uniform(0.3, 0.5))
                await element.press('Backspace')
                await asyncio.sleep(random.uniform(0.05, 0.1))

            await element.type(char)
            if char == " ":
                await asyncio.sleep(random.uniform(0.10, 0.2))
            await asyncio.sleep(random.uniform(0.15, 0.25))

    async def check_login(self):
        compose_button = await self.page.query_selector(self._SELECTORS['compose'])
        return compose_button is not None

    async def login(self):
        logger.info('Logging in...')
        await self._bg_delay()
        sign_in_button = await self.page.query_selector(self._SELECTORS['sign_in'])
        if sign_in_button is not None:
            await self._move_and_click(sign_in_button)

        email_input = await self.page.wait_for_selector(self._SELECTORS['login'])
        await self._move_and_type(email_input, self.__creds['login'])

        password_button = await self.page.wait_for_selector(self._SELECTORS['next'])
        await self._move_and_click(password_button)

        password_input = await self.page.wait_for_selector(self._SELECTORS['password'])
        await self._move_and_type(password_input, self.__creds['password'])
        password_button = await self.page.wait_for_selector(self._SELECTORS['next'])
        await self._move_and_click(password_button)

        logger.success('Logged in')

    async def initialise(self):
        logger.info('Starting Gmail...')
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch_persistent_context(
            user_data_dir='../../data/user_data',
            headless=False,
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-web-security",
                "--disable-dev-profile",
                "--disable-extensions"
            ]
        )
        logger.success('Gmail initialised')
        await self._bg_delay()

        self.page = await self.browser.new_page()
        await self._bg_delay()

        self.cursor = create_cursor(self.page)
        await self.page.goto("https://mail.google.com/mail/u/0/?pli=1")
        await self._bg_delay()

        check_login = await self.check_login()
        if not check_login:
            await self.login()

    async def sent_email(self, recipient, subject, message: str, name=""):
        logger.info(f'Sending email to {recipient}')
        compose_button = await self.page.query_selector(self._SELECTORS['compose'])
        await self._move_and_click(compose_button)

        recipient_input = await self.page.wait_for_selector(self._SELECTORS['recipient'])
        await self._move_and_type(recipient_input, recipient)
        await self._sm_delay()
        await self.page.keyboard.press('Enter')
        await self._bg_delay()

        subject_input = await self.page.wait_for_selector(self._SELECTORS['subject'])
        await self._move_cursor_randomly_left()
        await self._move_and_type(subject_input, subject, allow_paste=False)

        message_input = await self.page.wait_for_selector(self._SELECTORS['message'])

        message = message.replace('{name}', f'{name}')
        await self._move_and_type(message_input, message)
        await self._bg_delay()

        send_button = await self.page.wait_for_selector(self._SELECTORS['send'])
        await self._move_and_click(send_button)
        logger.success(f'Sent email to {recipient}')
