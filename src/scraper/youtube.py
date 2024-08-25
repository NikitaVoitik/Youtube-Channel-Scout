from src.scraper.playwright_core import PlwCore
from utils.logger import get_logger

logger = get_logger()


class Youtube(PlwCore):
    def __init__(self, selectors: dict = {}):
        super().__init__()
        self._SELECTORS = selectors

    async def initialise(self):
        logger.info('Initialising Youtube...')
        await super().initialise()
        await self._page.goto("https://youtube.com/")
        await self._bg_delay()
        logger.success('Youtube initialised')

        # check_login = await self.check_login()
        # if not check_login:
        #     await self.login()
