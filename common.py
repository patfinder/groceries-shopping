
def open_and_wait(driver, url, waiter=None):
    """
    Open specified page and wait for ready (if provided)
    :param driver: web driver
    :param url: Url to open
    :param waiter: wait function to be called.
    :return: None
    """
    driver.get(url)
    if waiter:
        waiter()


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
