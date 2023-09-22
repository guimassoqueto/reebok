from asyncio import create_task, gather, run, Semaphore
from app.app import get_urls, app
from app.logging.logger import getLogger
from app.settings import MAX_CONCURRENCY


logger = getLogger("main.py")
CONCURRENCY_LIMIT = Semaphore(MAX_CONCURRENCY)

async def main():
  urls = get_urls()
  tasks = []
  for url in urls:
      task = create_task(app(url, CONCURRENCY_LIMIT))
      tasks.append(task)
  result = await gather(*tasks)
  return result


if __name__ == "__main__":
  logger.info("Iniatilizing app...")
  try:
    app = run(main())
    if app: logger.info("Application completed")
  except Exception as e:
    logger.error(e, exc_info=True)