import time
import requests

from selenium import webdriver
from bs4 import BeautifulSoup, NavigableString, Tag
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_iframe_source(soup: BeautifulSoup):
    iframe = soup.find_all('iframe')[0]
    try:
        src = iframe['src']
        return src
    except Exception as e:
        print(f"Error when finding iframe src: {e}")



def create_selenium_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    return options

    options.add_argument('--headless')
    options.add_argument("--incognito")
    options.add_argument("--nogpu")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1280")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    return options


def create_selenium_driver():
    options = create_selenium_options()
    ua = UserAgent()
    userAgent = ua.random
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
    return driver

def create_soup_from_source(url: str):
    driver = create_selenium_driver()
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'tab-controller-container-week'))
        )
        element.click()
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'tgTable'))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        return soup
    finally:
        driver.quit()


def find_calendar_container(soup: BeautifulSoup):
    calendar_container = soup.find(id='tgTable')
    if calendar_container is None:
        print(f"Calendar container not founded")
    return calendar_container


def find_month_rows(container: Tag | NavigableString):
    days_columns = container.find_all(class_ = 'tg-col')
    current_days_columns = container.find_all(class_ = 'tg-col-today')
    total_columns = days_columns + current_days_columns
    print(len(total_columns))
    

def main():
    url = 'https://www.gob.pe/institucion/presidencia/agenda'
    request = requests.get(url=url)
    soup = BeautifulSoup(request.text, features='html.parser')
    iframe_source = find_iframe_source(soup=soup)
    calendar_soup = create_soup_from_source(url=iframe_source)
    calendar_container = find_calendar_container(soup=calendar_soup)
    find_month_rows(container=calendar_container)


if __name__ == "__main__":
    main()