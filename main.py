import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import org.openqa.selenium.JavascriptExecutor;

# sys.path += ['~/myrepos/groceries_shopping/chrome-linux64/chrome']
def main():
    options = Options()
    options.add_argument('user-data-dir=/home/vuong/myrepos/groceries_shopping/ChromeProfile')
    options.add_experimental_option("detach", True)

    try:
        # browser = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)
        driver = webdriver.Chrome(options)
        # open_page(driver)

        # assert "Python" in driver.title
        # elem = driver.find_element(By.NAME, "q")
        # elem.clear()
        # elem.send_keys("pycon")
        # elem.send_keys(Keys.RETURN)
        # assert "No results found." not in driver.page_source

        load_all_products(driver)

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
        try:
            p_name = product.find_element(By.CSS_SELECTOR, ".product-bottom .product-title").text
            image = product.find_element(By.CSS_SELECTOR, ".product-top .product-image img")
            image_url = image.get_attribute('data-srcset')
            
            try: details = product.find_element(By.CSS_SELECTOR, ".product-bottom .price-box .price-regular span").text
            except: details = '<unknown>'

            print(f'Name: {p_name}, Price: {details}, Image: {image_url}')

        except Exception as ex:
            print(f'Exception: {ex}')
    
    print('Finished')


def load_all_products(driver):
    try:
        scroll_btn = driver.find_element(By.CSS_SELECTOR, '.infinite-scrolling')
        # Repeating scrolling 'load more' into view and wait, until ... TODO
        scroll_to_view(driver, scroll_btn)
    except Exception as ex:
        print(f'Exception: {ex}')


def scroll_to_view(driver, elem):
    """
    Scroll an element into view
    :param driver: web driver
    :param elem: element to scroll to view
    :return:
    """
    try:
        # driver as JavascriptExecutor
        driver.execute_script("arguments[0].scrollIntoView();", elem)
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
 