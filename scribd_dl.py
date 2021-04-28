from json import JSONDecodeError
from selenium.webdriver import Chrome

from webdriver_manager.chrome import ChromeDriverManager

from args_parser import ArgsParser

args = ArgsParser()

try:
    driver = Chrome(ChromeDriverManager().install())
except JSONDecodeError:
    try:
        driver = Chrome("./chromedriver")
    except Exception:
        driver = Chrome("chromedriver.exe")
input("Press enter to continue...")
driver.get("https://scribd.com")
