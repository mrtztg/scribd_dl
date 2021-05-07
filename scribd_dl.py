from json import JSONDecodeError
from time import time, sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from downloader import download_file
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

from args_parser import ArgsParser

args = ArgsParser()


def print_if_verbose(val):
    if args.output_verbose:
        print(val)


WAITING_TIMEOUT = 120
chrome_options = Options()
driver_user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36')
chrome_options.add_argument(f'user-agent={driver_user_agent}')
if not args.display_browser:
    chrome_options.add_argument('--headless')
try:
    driver = Chrome(ChromeDriverManager().install(), options=chrome_options)
except JSONDecodeError:
    try:
        driver = Chrome("./chromedriver", options=chrome_options)
    except Exception:
        driver = Chrome("chromedriver.exe", options=chrome_options)
try:
    print_if_verbose('opening website...')
    driver.get("https://scribd.com")
    login_btn_el = WebDriverWait(driver, WAITING_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.header_login_btn'))
    )
    print_if_verbose('logging in...')
    login_btn_el.click()
    login_email_btn_el = WebDriverWait(driver, WAITING_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.make_scribd_feel_alive a[data-e2e=email-button]'))
    )
    login_email_btn_el.click()
    driver.find_element_by_css_selector('.sign_in .login_or_email.email input').send_keys(
        args.acc_username)
    driver.find_element_by_css_selector('.sign_in .wrapper__password_input input').send_keys(
        args.acc_password)
    driver.find_element_by_css_selector('.sign_in button[type=submit]').click()
    # driver.find_element_by_css_selector('.sign_in button[type=submit]').click()

    sleep(1)

    books_url_list = args.get_books_url()
    if not books_url_list or books_url_list is None:
        print('input file is empty')
        exit(1)

    for book_url in books_url_list:
        print_if_verbose(f'Opening {book_url}')
        driver.get(book_url)
        listen_btn_el = WebDriverWait(driver, WAITING_TIMEOUT).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[data-e2e=primary-actions]>a[data-e2e=listen-button]'))
        )
        listen_btn_link = listen_btn_el.get_attribute('href')
        book_name = driver.find_element_by_css_selector('h1[data-e2e=desktop-content-title]').text
        driver.get(listen_btn_link)
        chapters_menu_el = WebDriverWait(driver, WAITING_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.header .menu_icon_container a.menu_icon'))
        )
        chapters_name = []
        chapters_audio_url = []
        chapters_menu_el.click()


        def get_chapters_list_el():
            _chapters_list_el = []
            while not _chapters_list_el:
                _chapters_list_el = driver.find_elements_by_css_selector(
                    '.header .menu_icon_container '
                    '.button_menu.bottom '
                    '.button_menu_items_container '
                    'ul.button_menu_items>li>a')
                sleep(.1)
            return _chapters_list_el


        chapters_list_el = get_chapters_list_el()

        for chapter_el in chapters_list_el:
            chapters_name.append(chapter_el.find_element_by_css_selector('span.track').text)
        for i, chapter_name in enumerate(chapters_name):
            chapters_list_el = get_chapters_list_el()
            chapters_list_el[i].click()

            start_time = time()
            added_audio = False
            while time() - start_time < 160 and not added_audio:
                audio_file_el = WebDriverWait(driver, WAITING_TIMEOUT).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'audio#audioplayer'))
                )
                audio_file_url = audio_file_el.get_attribute('src')
                if audio_file_url not in chapters_audio_url:
                    chapters_audio_url.append(audio_file_url)
                    added_audio = True
                sleep(.1)
            chapters_menu_el.click()
        driver.get(book_url)
        print('collected these chapters:')
        for i in range(len(chapters_name)):
            download_file(book_name, chapters_audio_url[i], f'{i + 1}-{chapters_name[i]}')
finally:
    driver.close()
