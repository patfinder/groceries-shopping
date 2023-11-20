import re
from datetime import datetime

from selenium.webdriver.common.by import By

from common import scroll_up, scroll_to_view
from dbconnect import Product, add_products

RETAILER_NAME = 'alpremium'


def load_all_products(driver):

    def get_product_count():
        products = driver.find_elements(By.CSS_SELECTOR, '.grid-item')
        return len(products)

    try:
        scroll_btn = driver.find_element(By.CSS_SELECTOR, '.infinite-scrolling')

        # Repeat N times
        # last_prod_count = 0
        for i in range(0, 100):
            # Repeating scrolling 'load more' into view and wait, until ... TODO
            scroll_to_view(driver, scroll_btn)
            # Must scroll up a bit
            scroll_up(driver)

            # Wait for the Dom to be updated
            driver.implicitly_wait(1)

            # Count the number of product items
            product_count = get_product_count()
            # product_count == last_prod_count
            if scroll_btn.text == "NO MORE PRODUCT":
                # No more product loaded. Stop
                # Also, check scroll_btn.text == "NO MORE PRODUCT"
                break
            # else:
            #     last_prod_count = product_count

    except Exception as ex:
        print(f'Exception: {ex}')


def get_items(driver, retailer, category):
    web_products = driver.find_elements(By.CSS_SELECTOR, '.grid-item')
    products = []
    for web_product in web_products:
        try:
            name_el = web_product.find_element(By.CSS_SELECTOR, '.product-bottom .product-title')
            # Check if product is visible
            if not name_el.is_displayed():
                continue

            name = name_el.text
            url = (web_product.find_element(By.CSS_SELECTOR, '.product-top>.product-image>a.product-grid-image')
                   .get_attribute('href'))
            image = web_product.find_element(By.CSS_SELECTOR, '.product-top>.product-image img')
            image_url = image.get_attribute('data-srcset')

            # Get price
            price_els = web_product.find_elements(By.CSS_SELECTOR,
                                                  '.product-bottom .price-box .price-regular>span')
            price_el = next(filter(lambda e: e.get_attribute('style') == '', price_els))
            price = float(price_el.text.strip('$'))

            # TODO: old-price

            # unit_text is something like: '$0.32 / ea\n$0.79/lb'
            unit_text = web_product.find_element(By.CSS_SELECTOR, '.product-bottom .price-box>div').text
            unit = parse_price(unit_text)

            product = Product(retailer=retailer, name=name, categories=category, image=image_url, url=url,
                              price=price, old_price=price, unit=unit, created_time=datetime.now())
            products.append(product)

            # TODO: test
            # if len(products) >= 10:
            #     return products

        except Exception as ex:
            print(f'Exception: {ex}')

    return products


def process_category(driver, retailer, url):
    try:
        driver.get(url)
        # driver.Manage().Window.Maximize()

        load_all_products(driver)

        products = get_items(driver, retailer, parse_category(url))
        print(f'Read {len(products)} products')

        add_products(products)
    except Exception as ex:
        print(f'Exception: {ex}')


def process_site(driver):
    urls = [
        'https://mi.alpremium.ca/collections/fruit',
        # 'https://mi.alpremium.ca/collections/vegetable',
        # 'https://mi.alpremium.ca/collections/fresh-meat',
        # 'https://mi.alpremium.ca/collections/seafood',
        # 'https://mi.alpremium.ca/collections/frozen-food',
        # 'https://mi.alpremium.ca/collections/grocery',
    ]

    for url in urls:
        print(f'Start processing for url: {url}')
        process_category(driver, RETAILER_NAME, url)
        print(f'Processing done for url: {url}')


def parse_category(url):
    try:
        return re.match(r'^.*/([^/]+)$', url).group(1)
    except Exception:
        return '<unknown>'


def parse_price(price_box_text):
    try:
        # '$0.32 / ea\n$0.79/lb'
        res = re.match(r'^\$([.0-9]+) (.+)', price_box_text)
        return res.group(2).lstrip('/ ')
    except Exception:
        # TODO: unknown unit
        return '<unknown>'
