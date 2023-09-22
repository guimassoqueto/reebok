from playwright.async_api import async_playwright
from app.infra.playwright.random_header import fake_header
from app.logging.logger import getLogger
from time import sleep
logger = getLogger("playwright.py")


class Playwright:
  @staticmethod
  async def get_content(url: str) -> str:
    """
    Get the web page full content, dynamic or not.
    """
    logger.info(f"Extracting: {url}")
    async with async_playwright() as pw:
      browser = await pw.firefox.launch(headless=True)
      page = await browser.new_page()
      await page.set_viewport_size({ "width": 1920, "height": 8000 })
      await page.goto(url)
      await page.wait_for_selector('.vtex-search-result-3-x-galleryItem:nth-child(12)', timeout=20000)
      html_content =  await page.content()
      return html_content
