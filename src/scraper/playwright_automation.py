from playwright.async_api import async_playwright, Page, BrowserContext, Playwright
import asyncio
import random
from python_ghost_cursor.playwright_async import create_cursor
from python_ghost_cursor.playwright_async._spoof import GhostCursor


class PlaywrightAutomation:
    def __init__(self):
        self.cursor: GhostCursor | None = None
        self.playwright_instance: Playwright | None = None
        self.page: Page | None = None
        self.browser: BrowserContext | None = None

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

    async def initialise(self):
        self.playwright_instance = await async_playwright().start()
        self.browser = await self.playwright_instance.chromium.launch_persistent_context(
            user_data_dir='../../../data/user_data',
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
        await self._bg_delay()

        self.page = await self.browser.new_page()
        await self._bg_delay()

        self.cursor = create_cursor(self.page)
        await self._bg_delay()
