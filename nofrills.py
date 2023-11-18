from datetime import datetime

from selenium.webdriver.common.by import By
from common import scroll_to_view, scroll_up
from dbconnect import Product, add_products

RETAILER_NAME = 'nofrills'


def test_nofrills(driver):
    pass


def process_site(driver):
    # dict of category and url
    urls = {
        'fresh-vegetables': 'https://www.nofrills.ca/food/fruits-vegetables/fresh-vegetables/c/28195',
    }

    def check_page_and_wait(page):
        # Check if page exist?
        try:
            nav_button = driver.find_element(
                By.CSS_SELECTOR, f'nav[data-testid="pagination"]>button[aria-label="Page {page}"]')
            nav_button.click()

            # wait 30 time/seconds
            for ww in range(30):
                driver.implicitly_wait(1)

                # Check if button disabled
                try:
                    nav_button = driver.find_element(
                        By.CSS_SELECTOR, f'nav[data-testid="pagination"]>button[aria-label="Page {page}"]')
                    # page loaded
                    if nav_button.get_attribute('aria-current') == 'true':
                        break
                except Exception:
                    pass

            return True

        except Exception as ex:
            print(f'Exception while opening page {page} (will Stop): {ex}')
            return False

    def loop_on_pages(category, url):
        # Loop 100 page?
        for page in range(1, 101):
            try:
                if page == 1:
                    process_category(driver, RETAILER_NAME, category, url)
                elif check_page_and_wait(page):
                    process_category(driver, RETAILER_NAME, category, f'url?page={page}')

            except Exception as ex:
                print(f'Exception: {ex}')

    for category, url in urls.items():
        print(f'Start processing for url: {url}')
        loop_on_pages(category, url)
        print(f'Processing done for url: {url}')


def process_category(driver, retailer, category, url):
    try:
        products = get_items(driver, retailer, category)
        print(f'Read {len(products)} products')

        add_products(products)
    except Exception as ex:
        print(f'Exception: {ex}')


def get_items(driver, retailer, category):
    web_products = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="product-grid"]>div')
    products = []
    for web_product in web_products:
        try:
            name = web_product.find_element(By.CSS_SELECTOR, 'h3[data-testid="product-title"]').text

            image = (web_product.find_element(By.CSS_SELECTOR, 'div[data-testid="product-image"]>img')
                     .get_attribute('src'))

            price = web_product.find_element(By.CSS_SELECTOR, 'p[data-testid="price"]').text
            price = float(price.replace('sale\n', '').replace('about', '').lstrip(' $'))

            try:
                old_price = web_product.find_element(By.CSS_SELECTOR, 'p[data-testid="was-price"]').text
                old_price = float(price.lstrip(' $'))
            except Exception:
                old_price = price

            url = (web_product.find_element(By.CSS_SELECTOR, 'div[data-testid="price-product-tile"]+a')
                   .get_attribute('href'))

            unit = web_product.find_element(By.CSS_SELECTOR, 'p[data-testid="product-package-size"]').text
            unit = unit.split(',')[0].lstrip('1 ')

            product = Product(id=url, retailer=retailer, name=name, categories=category, image=image, url=url,
                              price=price, old_price=old_price, unit=unit, created_time=datetime.now())
            products.append(product)

            # TODO: test
            # if len(products) >= 10:
            #     return products

        except Exception as ex:
            print(f'Exception: {ex}')

    return products
