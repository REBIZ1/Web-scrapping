from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_chrome_driver():
    """
    возваращает драйвер браузера Chrome
    """
    chrome_path = ChromeDriverManager().install()
    service = Service(executable_path=chrome_path)
    browser = Chrome(service=service)
    return browser

