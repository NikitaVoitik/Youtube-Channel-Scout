import asyncio

from selenium.webdriver.common.devtools.v125.runtime import await_promise

from src.scraper.playwright_core import PlwCore
from utils.logger import get_logger

logger = get_logger()


class Youtube(PlwCore):
    def __init__(self, selectors: dict):
        super().__init__()
        self._SELECTORS = selectors

    async def initialise(self):
        logger.info('Initialising Youtube...')
        await super().initialise()
        await self._page.goto("https://youtube.com/")
        await self._bg_delay()
        cookies = await self._page.wait_for_selector(self._SELECTORS['cookies_accept'])
        await self._move_and_click(cookies)
        await self._bg_delay()
        logger.success('Youtube initialised')

    async def _check_premier(self, premiers, video):
        for premier in premiers:
            if await self._is_child(premier, video):
                return True
        return False

    async def check_channel(self, channel):
        logger.info(f"Started checking channel {channel}")
        href = await channel.get_attribute('href')
        try:
            await self._move(channel)
            url = f'https://youtube.com/{href}/videos'
            new_page = await self._context.new_page()
            await new_page.goto(url)
            logger.info(f"Opened channel {href} videos page")
            videos = await new_page.query_selector_all(self._SELECTORS['video'])
            premiers = await new_page.query_selector_all(self._SELECTORS['notify_me'])
            for ind, video in enumerate(videos):
                if await self._check_premier(premiers, video):
                    logger.info(f"{video} is premiere")
                    continue


        except Exception as e:
            logger.error(f'Error {e} while checking channel {href}')

    async def search(self, queries: list[str], max_results_per_query: int = 50):
        for query in queries:
            logger.info(f'Searching for query: {query} on Youtube, with max results: {max_results_per_query}')
            searchbar = await self._page.wait_for_selector(self._SELECTORS['searchbar'])
            await self._move_and_type(searchbar, query)
            await self._bg_delay()

            search_button = await self._page.wait_for_selector(self._SELECTORS['search_button'])
            while 'results?search_query' not in self._page.url:
                await self._move_and_click(search_button)
                await self._bg_delay()

            channels = await self._page.query_selector_all(self._SELECTORS['channel'])
            await self._bg_delay()
            for channel in channels:
                await self.check_channel(channel)
