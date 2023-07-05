from time import time, sleep
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from args_parser import ArgsParser
from downloader import download_file

args = ArgsParser()


def print_if_verbose(val):
    if args.output_verbose:
        print(val)


WAITING_TIMEOUT = 180
chrome_options = Options()
driver_user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36')
chrome_options.add_argument(f'user-agent={driver_user_agent}')
if not args.display_browser:
    chrome_options.add_argument('--headless')
try:
    #driver = Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install(), options=chrome_options))
except Exception as e:
    print(e)
      try:
        driver = Chrome("./chromedriver", options=chrome_options, port=100)
    except Exception:
        driver = Chrome("chromedriver.exe", options=chrome_options, port=100)
actions = ActionChains(driver)


def click_on_el(el: WebElement):
    actions.move_to_element(el).click().perform()


try:
    print_if_verbose('opening website...')
    driver.get("https://scribd.com")
    login_btn_el = WebDriverWait(driver, WAITING_TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-e2e="landing-sign-in-button"]'))
    )
    print_if_verbose('logging in...')
    click_on_el(login_btn_el)
    login_email_btn_el = WebDriverWait(driver, WAITING_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[data-e2e=email-button]'))
    )
    click_on_el(login_email_btn_el)
    driver.find_element(By.CSS_SELECTOR, '.sign_in .login_or_email.email input').send_keys(
        args.acc_username)
    sleep(2)
    driver.find_element(By.CSS_SELECTOR, '.sign_in .wrapper__password_input input').send_keys(
        args.acc_password)
    sleep(3)
    click_on_el(driver.find_element(By.CSS_SELECTOR, '.sign_in button[type=submit]'))


    # driver.find_element_by_css_selector('.sign_in button[type=submit]').click()

    def logged_in_check():
        _start_time = time()
        logged_in = False
        while True:
            if 'scribd.com/home' in driver.current_url:
                logged_in = True
                break
            if abs(time() - _start_time) > 60:
                break
            sleep(1)
        if not logged_in:
            if args.display_browser:
                print("Solve the reCAPTCHA")
                logged_in_check()
            else:
                print("Run script again with '--display' parameter added. Because reCAPTCHA "
                      "solving needed")
                exit(1)


    logged_in_check()

    books_url_list = args.get_books_url()
    if not books_url_list or books_url_list is None:
        print('input file is empty')
        exit(1)

    for book_url in books_url_list:
        print_if_verbose(f'Opening {book_url}')
        driver.get(book_url)
        listen_btn_el = WebDriverWait(driver, WAITING_TIMEOUT).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[data-e2e=listen-button]'))
        )
        listen_btn_link = listen_btn_el.get_attribute('href')
        book_name = driver.find_element(By.CSS_SELECTOR, 'h1[data-e2e=desktop-content-title]').text
        driver.get(listen_btn_link)
        chapters_menu_el = WebDriverWait(driver, WAITING_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.header .menu_icon_container a.menu_icon'))
        )
        chapters_name = []
        chapters_audio_url = []
        click_on_el(chapters_menu_el)


        def get_chapters_list_el() -> list[WebElement]:
            _chapters_list_el = []
            while not _chapters_list_el:
                _chapters_list_el = driver.find_elements(By.CSS_SELECTOR,
                                                         '.header .menu_icon_container '
                                                         '.button_menu.bottom '
                                                         '.button_menu_items_container '
                                                         'ul.button_menu_items>li>a')
                sleep(.1)
            return _chapters_list_el


        chapters_list_el = get_chapters_list_el()

        for chapter_el in chapters_list_el:
            chapters_name.append(chapter_el.find_element(By.CSS_SELECTOR, 'span.track').text)
        for i, chapter_name in enumerate(chapters_name):
            chapters_list_el = get_chapters_list_el()
            click_on_el(chapters_list_el[i])

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
            click_on_el(chapters_menu_el)
        driver.get(book_url)
        print('collected these chapters:')
        for i in range(len(chapters_name)):
            download_file(book_name, chapters_audio_url[i], f'{i + 1}-{chapters_name[i]}')
finally:
    driver.close()
