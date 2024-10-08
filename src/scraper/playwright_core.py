from playwright.async_api import async_playwright, Page, BrowserContext, Playwright, Browser
import asyncio
import random
from python_ghost_cursor.playwright_async import create_cursor
from python_ghost_cursor.playwright_async._spoof import GhostCursor


class PlwCore:
    _playwright_instance: Playwright | None = None
    _browser: Browser

    def __init__(self):
        self._context: BrowserContext | None = None
        self._page: Page | None = None
        self._cursor: GhostCursor | None = None

    @staticmethod
    async def _sm_delay():
        await asyncio.sleep(random.uniform(0.1, 0.4))

    @staticmethod
    async def _md_delay():
        await asyncio.sleep(random.uniform(0.5, 1.1))

    @staticmethod
    async def _bg_delay():
        await asyncio.sleep(random.uniform(1.1, 1.8))

    @staticmethod
    async def _get_outer_html(element):
        await element.evaluate('(element) => element.outerHTML')

    async def _is_child(self, child, parent):
        is_child = await self._page.evaluate(
            '''(parent, child) => parent.contains(child)''',
            [parent, child]
        )
        return is_child

    async def _move(self, element, padding_percentage: int = 0):
        await self._sm_delay()
        await self._cursor.move(element, padding_percentage=padding_percentage)
        await self._md_delay()

    async def _move_and_click(self, element, padding_percentage: int = 0):
        await self._sm_delay()
        await self._cursor.click(element, wait_for_click=random.randint(200, 600),
                                 padding_percentage=padding_percentage)
        await self._md_delay()

    async def _move_and_type(self, element, text, allow_paste=True, padding_percentage: int = 0):
        await self._move_and_click(element, padding_percentage)
        await self._sm_delay()
        await self._type_text(element, text, allow_paste)
        await self._md_delay()

    async def _typing_mistake(self, element, chance=3):
        if random.randint(1, 100) < chance:
            wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz ')
            await element.type(wrong_char, chance=20)
            await asyncio.sleep(random.uniform(0.5, 1.2))
            await self._typing_mistake(element)
            await element.press('Backspace')
            await asyncio.sleep(random.uniform(0.5, 0.15))

    async def _move_to_random_element(self):
        elements = await self._page.query_selector_all('div')
        random_element = random.choice(elements)
        await self._cursor.move_to(random_element)
        await self._md_delay()

    async def _type_text(self, element, text, allow_paste=True):
        if allow_paste:
            chance = random.randint(1, 100)
            if chance <= 30:
                await element.fill(text)
                print('paste')
                return
        for char in text:
            await self._typing_mistake(element)

            await element.type(char)
            if char == " ":
                await asyncio.sleep(random.uniform(0.10, 0.2))
            await asyncio.sleep(random.uniform(0.15, 0.25))

    async def initialise(self):
        PlwCore._playwright_instance = await async_playwright().start()
        PlwCore._browser = await PlwCore._playwright_instance.chromium.launch(headless=False,
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
        self._context = await PlwCore._browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        )
        self._page = await self._context.new_page()
        await self._page.set_viewport_size({"width": 1280, "height": 800})
        await self._bg_delay()

        self._cursor = create_cursor(self._page)
        await self._bg_delay()
