import re
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from dbconnect import Product, add_products


# sys.path += ['~/myrepos/groceries_shopping/chrome-linux64/chrome']
def main():
    options = Options()
    # options.add_argument('user-data-dir=/home/vuong/myrepos/groceries_shopping/ChromeProfile')
    # options.add_experimental_option('detach', True)
    options.binary_location = '/usr/bin/google-chrome-stable'
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')

    try:
        # browser = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)
        driver = webdriver.Chrome(options)
        # open_page(driver)

        load_all_products(driver)

        products = get_items(driver)
        add_products(products)

        # driver.close()
    except Exception as ex:
        print(f'Exception: {ex}')


def open_page(driver):
    driver.get('https://google.com/')
    driver.get('https://www.walmart.ca/')
    driver.get('https://www.walmart.ca/en/browse/grocery/fruits-vegetables/fresh-fruits/10019_6000194327370_6000194327411')
    driver.get('https://www.nofrills.ca/print-flyer')
    driver.get('https://mi.alpremium.ca/collections/fruit')
    # driver.Manage().Window.Maximize()


ALPREMIUM = 'alpremium'


def parse_price(price_box_text):
    try:
        # '$0.32 / ea\n$0.79/lb'
        res = re.match(r'^\$([.0-9]+) (.+)', price_box_text)
        return res.group(2).lstrip('/ ')
    except Exception:
        # TODO: unknown unit
        return '<unknown>'


def get_items(driver):
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
            # unit_text is something like: '$0.32 / ea\n$0.79/lb'
            unit_text = web_product.find_element(By.CSS_SELECTOR, '.product-bottom .price-box>div').text
            unit = parse_price(unit_text)

            # TODO: retailer, categories
            product = Product(id=url, retailer=ALPREMIUM, name=name, categories='fruit', image=image_url, url=url,
                              price=price, unit=unit)
            products.append(product)

            # TODO: test
            if len(products) >= 10:
                return products

            # print(f'Name: {name}, Price: {details}, Image: {image_url}')

        except Exception as ex:
            print(f'Exception: {ex}')

    print('Finished')
    return products


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


def scroll_up(driver, pixels=-350):
    driver.execute_script(f'window.scrollBy(0, {pixels})', '')


def scroll_to_view(driver, elem):
    """
    Scroll an element into view
    :param driver: web driver
    :param elem: element to scroll to view
    :return:
    """
    try:
        # driver as JavascriptExecutor
        driver.execute_script('arguments[0].scrollIntoView();', elem)
    except Exception as ex:
        print(f'Exception: {ex}')
        pass


def is_element_in_viewport(driver, elem):
    """
    Check if an element (elem) is visible in the view port
    :param driver: web driver
    :param elem: element to check
    :return: True if visible, False otherwise
    """
    driver.execute_script("""
        var elem = arguments[0],
              box = elem.getBoundingClientRect(),
              cx = box.left + box.width / 2,
              cy = box.top + box.height / 2,
              e = document.elementFromPoint(cx, cy);
        for (; e; e = e.parentElement) {
              if (e === elem)
                    return true;
        }
        return false;
    """, elem)


if __name__ == '__main__':
    main()
 