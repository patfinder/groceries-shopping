# import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import alpremium
import nofrills


# from selenium.webdriver.common.keys import Keys


# sys.path += ['~/myrepos/groceries_shopping/chrome-linux64/chrome']
def main():
    options = Options()
    # options.add_argument('user-data-dir=/home/vuong/tmp/ChromeProfile')
    # options.add_experimental_option('detach', True)
    options.binary_location = '/usr/bin/google-chrome-stable'
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')

    try:
        # browser = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)
        driver = webdriver.Chrome(options)
        # open_page(driver)

        alpremium.process_site(driver)
        nofrills.process_site(driver)

        # driver.close()
    except Exception as ex:
        print(f'Exception: {ex}')


if __name__ == '__main__':
    main()
 