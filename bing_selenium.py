# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# парсер bing по ключу, первые 10 сайтов

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep

keyword = 'яблочный+уксус+свойства+и+применение'


def init_driver():  # инициализация экземпляра драйвера
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # для открытия headless-браузера
    driver = webdriver.Firefox(options=options)
    driver.wait = WebDriverWait(driver, 3)
    return driver


def input_key(driver, keyword):  # получаем выдачу по ключу
    driver.get('https://www.bing.com/')  # начальная пага
    fild = driver.find_element_by_id('sb_form_q')
    enter = driver.find_element_by_xpath('//*[@id="sb_form"]/label')
    fild.send_keys(keyword)
    sleep(3)
    enter.click()


def get_html(url):  # получаем код страницы
    driver.get(url)
    html = driver.page_source
    return html


def parse(url):  # парсинг
    result = []
    soup = BeautifulSoup(get_html(url), 'lxml')
    blocks = soup.find_all(class_='b_algo')
    for block in blocks:
        urls = block.find_all('a')
        url = urls[0].get('href')
        result.append(url)
        print(url)
    return result


def main():
    url = f'https://www.bing.com/search?q={keyword}'
    result = parse(url)
    return result


if __name__ == "__main__":
    try:
        driver = init_driver()  # инициализация драйвера
        input_key(driver, keyword)  # получаем выдачу по ключу
        print('Результаты по запросу ', keyword)

        result = main()  # сам парсинг, получаем список url

    finally:
        driver.quit()  # закрываем браузер в любом случае
