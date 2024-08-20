from playwright.async_api import async_playwright, Page, BrowserContext
import asyncio
import random
from utils.logger import get_logger
from utils.load_data import load_json

logger = get_logger()

class Gmail:
    def __init__(self):
        self._SELECTORS = load_json('selectors.json')['gmail']
        self.page: Page | None = None
        self.browser: BrowserContext | None = None

    @staticmethod
    async def _sm_delay():
        await asyncio.sleep(random.uniform(0.1, 0.6))

    @staticmethod
    async def _md_delay():
        await asyncio.sleep(random.uniform(0.6, 1.2))

    @staticmethod
    async def _bg_delay():
        await asyncio.sleep(random.uniform(1.2, 2))

    async def _mouse_move(self, element):
        box = await element.bounding_box()
        x = random.uniform(box['x'], box['x'] + box['width'])
        y = random.uniform(box['y'], box['y'] + box['height'])

        await self.page.mouse.move(x, y, steps=random.randint(15, 25))

    async def _move_and_click(self, element):
        await self._mouse_move(element)
        await self._md_delay()
        await element.click()
        await self._sm_delay()


    async def _move_and_type(self, element, text):
        await self._move_and_click(element)
        await self._sm_delay()
        await self._type_text(element, text)
        await self._md_delay()

    @staticmethod
    async def _type_text(element, text):
        await element.type(text, delay=random.randint(150, 250))


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
        await self._move_and_type(email_input, 'kevin.cryptonomy.finance@gmail.com')

        password_button = await self.page.wait_for_selector(self._SELECTORS['next'])
        await self._move_and_click(password_button)


        password_input = await self.page.wait_for_selector(self._SELECTORS['password'])
        await self._move_and_type(password_input, 'PepsiJesusMango')
        password_button = await self.page.wait_for_selector(self._SELECTORS['next'])
        await self._move_and_click(password_button)

        logger.success('Logged in')

    async def initialise(self):
        async with async_playwright() as p:
            logger.info('Starting Gmail...')
            self.browser = await p.chromium.launch_persistent_context(
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

            await self.page.goto("https://mail.google.com/mail/u/0/?pli=1")
            await self._bg_delay()

            check_login = await self.check_login()
            if not check_login:
                await self.login()

            await asyncio.sleep(100)

            await self.browser.close()
            logger.success('Gmail closed')
