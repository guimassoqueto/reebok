import re


def get_image_url(small_image_url: str) -> str:
  return small_image_url.replace("300-300", "1080-1080").replace("width=300", "width=1080").replace("height=300", "height=1080")

def get_price(inner_text: str) -> str:
  raw_price = re.search(r"[\d,.]+", inner_text).group()
  price = raw_price.replace(".", "").replace(",", ".")
  return float(price)