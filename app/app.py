from asyncio import Semaphore
from app.infra.playwright.playwright import Playwright
from app.infra.selectolax.parser import Selectolax
from app.settings import REBOOK_OUTLET_PAGE
from app.infra.psycopg.postgres import insert_products
from app.logging.logger import getLogger


logger = getLogger("app.py")


def get_urls():
  return [f"{REBOOK_OUTLET_PAGE}{i}" for i in range(1, 7)]


async def app(url: str, concurrency_limit: Semaphore):
  async with concurrency_limit:
    try:
      content = await Playwright.get_content(url)
      products = Selectolax.get_products(content)
      await insert_products(products)
    except Exception as e:
      logger.error(e)
      raise e