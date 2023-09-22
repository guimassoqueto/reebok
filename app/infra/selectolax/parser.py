from selectolax.parser import HTMLParser
from urllib.parse import urljoin
from app.domain.model import Item
from app.logging.logger import getLogger
from app.infra.selectolax.helpers import get_image_url, get_price

logger = getLogger("parser.py")

BASE_URL = "https://www.reebok.com.br/"


class Selectolax:
  @staticmethod
  def get_products(content: str) -> list:
    parser = HTMLParser(content)
    items = parser.css('.vtex-search-result-3-x-galleryItem')
    products = []
    for item in items:
      try:
        url = urljoin(BASE_URL, item.css_first('a').attrs['href'])
        afiliate_url = url
        title = item.css_first('h3').text()
        category = f"Reebok Outlet {title}"
        image_url = get_image_url(item.css_first("img.vtex-product-summary-2-x-imageNormal").attrs["src"])
        reviews = 0
        free_shipping=False
        price=get_price(item.css_first('span.vtex-product-price-1-x-sellingPriceValue').text())
        previous_price=get_price(item.css_first('span.vtex-product-price-1-x-listPrice').text())
        discount = round((1 - (price / previous_price)) * 100)
        if discount < 30: continue
        
        item = Item(
          url=url,
          afiliate_url=afiliate_url,
          title=title,
          category=category,
          image_url=image_url,
          reviews=reviews,
          free_shipping=free_shipping,
          price=price,
          previous_price=previous_price,
          discount=discount
        )
        products.append(item.model_dump())
      
      except Exception as e:
        logger.warning(e)
        continue

    return products

