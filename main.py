import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# sys.path += ['~/myrepos/groceries_shopping/chrome-linux64/chrome']
def main():
    options = Options()
    options.add_argument('user-data-dir=/home/vuong/myrepos/groceries_shopping/ChromeProfile')

    try:
        driver = webdriver.Chrome(options)
        open_page(driver)

        # assert "Python" in driver.title
        # elem = driver.find_element(By.NAME, "q")
        # elem.clear()
        # elem.send_keys("pycon")
        # elem.send_keys(Keys.RETURN)
        # assert "No results found." not in driver.page_source

        get_items(driver)

        # driver.close()
    except Exception as ex:
        print(f'Exception: {ex}')


def open_page(driver):
    # driver.get("https://google.com/")
    # driver.get("https://www.walmart.ca/")
    # driver.get("https://www.walmart.ca/en/browse/grocery/fruits-vegetables/fresh-fruits/10019_6000194327370_6000194327411")
    # driver.get("https://www.nofrills.ca/print-flyer")
    driver.get("https://mi.alpremium.ca/collections/fruit")
    # driver.Manage().Window.Maximize()


def get_items(driver):
    products = driver.find_elements(By.CSS_SELECTOR, ".grid-item")
    for product in products:
        image = product.find_element(By.CSS_SELECTOR, ".product-top .product-image")
        details = product.find_element(By.CSS_SELECTOR, ".product-bottom .price-box .price-regular span")
        print(f'Image: {image}, price: {details}')


if __name__ == '__main__':
    main()
