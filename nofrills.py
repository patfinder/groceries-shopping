import time
from datetime import datetime

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from common import scroll_to_view, scroll_up, open_and_wait
from dbconnect import Product, add_products

RETAILER_NAME = 'nofrills'


def process_site(driver):
    # dict of category and url
    urls = {
        'fresh-vegetables': 'https://www.nofrills.ca/food/fruits-vegetables/fresh-vegetables/c/28195',
        # 'fresh-fruits': 'https://www.nofrills.ca/food/fruits-vegetables/fresh-fruits/c/28194',
        # 'meat': 'https://www.nofrills.ca/food/meat/c/27998',
        # 'dairy-eggs': 'https://www.nofrills.ca/food/dairy-eggs/c/28003',
        # 'fish-seafood': 'https://www.nofrills.ca/food/fish-seafood/c/27999',
        # 'pantry': 'https://www.nofrills.ca/food/pantry/c/28006',
        # 'drinks': 'https://www.nofrills.ca/food/drinks/c/28004',
    }

    for category, url in urls.items():
        print(f'Start processing for url: {url}')
        process_all_pages(driver, category, url)
        print(f'Processing done for url: {url}')


def process_all_pages(driver, category, url):

    def waiter():
        try:
            # Wait for 30 seconds
            for i in range(30):
                # Wait at least 1 second
                driver.implicitly_wait(1)
                time.sleep(1)

                # Check if "No items are available." item exist
                no_item = driver.find_elements(By.CSS_SELECTOR, 'p[data-testid="sub-heading"]')
                if len(no_item) and no_item[0].text == 'No items are available.':
                    break

                # Check if some product exist.
                web_products = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="product-grid"]>div')
                if not web_products:
                    continue

                try:
                    # Access first element
                    web_products[0].find_element(By.CSS_SELECTOR, 'h3[data-testid="product-title"]')
                    # No error, stop
                    break
                except NoSuchElementException:
                    continue
                except StaleElementReferenceException:
                    continue

        except Exception as ex:
            print(f'Exception while waiting: {ex}')

    # Loop 100 page?
    for page in range(1, 101):
        try:
            print(f'Processing page {page}')

            if page == 1:
                open_and_wait(driver, url, waiter)
                process_one_page(driver, RETAILER_NAME, category)
            elif click_page_and_wait(driver, page):
                process_one_page(driver, RETAILER_NAME, category)
            else:
                # no more items
                break

        except Exception as ex:
            print(f'Exception: {ex}')


def click_page_and_wait(driver, page):
    """
    Find and click on nav button for the page.
    :param driver: web driver
    :param page: page number, start from 1. Page number will be combined with base Url
    :return: True if button for the page exists, False  otherwise
    """
    try:
        # Check if page exist?
        nav_button = driver.find_element(
            By.CSS_SELECTOR, f'nav[data-testid="pagination"]>button[aria-label="Page {page}"]')
    except NoSuchElementException:
        return False

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


def process_one_page(driver, retailer, category):
    try:
        products = get_items(driver, retailer, category)
        print(f'Read {len(products)} products')

        # Save products
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

            old_price = web_product.find_elements(By.CSS_SELECTOR, 'p[data-testid="was-price"]')
            old_price = float(old_price[0].text.replace('was\n', '').lstrip(' $')) if len(old_price) else price

            url = (web_product.find_element(By.CSS_SELECTOR, 'div[data-testid="price-product-tile"]+a')
                   .get_attribute('href'))

            unit = web_product.find_element(By.CSS_SELECTOR, 'p[data-testid="product-package-size"]').text
            unit = unit.split(',')[0].lstrip('1 ')

            product = Product(retailer=retailer, name=name, categories=category, image=image, url=url,
                              price=price, old_price=old_price, unit=unit, created_time=datetime.now())
            products.append(product)

        except Exception as ex:
            print(f'Exception: {ex}')

    return products
