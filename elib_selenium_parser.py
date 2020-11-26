# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Парсер elibrary.ru на чистом selenium, получение ссылок вида
# https://elibrary.ru/item.asp?id=28153408 по ключевому слову
# на выходе сортирует по индексу цитирования  max > min

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import csv


keyword = ''

options = webdriver.FirefoxOptions()
# убирает детект вебдрайвера
options.set_preference('dom.webdriver.enabled', False)

# убирает всплывающие окна в браузере
options.set_preference('dom.webnotifications.enabled', False)

# можно юзать любой юзерагент
options.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4276.0 Safari/537.36')

# отключает звуки в браузере
options.set_preference('media.volume_scale', '0.0')
options.headless = True # безголовый браузер


def init_driver():  # инициализация экземпляра драйвера
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(3)
    return driver


def input_key(driver, keyword):  # получаем выдачу по ключу
    driver.get('https://www.elibrary.ru/defaultx.asp')  # начальная пага
    fild = driver.find_element_by_class_name('inputt')  # id='ftext'
    enter = driver.find_element_by_class_name('butblue')
    fild.send_keys(keyword)
    # sleep(3)
    enter.click()
    url = driver.current_url
    return url

# для записи результатов в csv файл
# def write_csv(data):
#     with open('elib_parse.csv', 'a') as f:
#         writer = csv.writer(f)
#         writer.writerow((data['link'], data['index']))


def parse(driver, url):  # парсинг страницы
    driver.get(url)

    result, links, indexes = [], [], []

    a_list = driver.find_elements_by_xpath("//*[@id='restab']//tr[not(@align)]//td[@align='left']/a")
    for a in a_list:
        try:
            link = a.get_attribute('href')
        except:
            link = 'Ссылка отсутствует'
        links.append(link)

    num_list = driver.find_elements_by_xpath("//*[@id='restab']//tr[not(@align)]//td[@valign='middle']")
    for num in num_list:
        try:
            index = int(num.get_attribute('textContent'))
        except:
            index = 'Индекс отсутствует'
        indexes.append(index)
    # проверка наличия на странице флага пагинации
    try:
        next_td = driver.find_element_by_xpath("//*[contains(text(), '>>')]")
        if next_td:  # если флаг есть
            next_url = next_td.get_attribute('href')
            # получаем ссылку на следующую страницу
    except:
        next_url = False  # если флага нет

    result = list(zip(links, indexes))

    return result, next_url


def main(driver, url):
    result = []
    while True:
        res, url = parse(driver, url)  # парсинг данных
        result += res

        # проверка наличия пагинации
        if not url:
            break
    return result  # весь результат парсинга, список кортежей


if __name__ == "__main__":
    try:
        driver = init_driver()  # инициализация драйвера
        url = input_key(driver, keyword)  # страница результатов по ключу
        print('Результаты по запросу ', keyword)

        result = main(driver, url)  # сам парсинг, получаем список кортежей
        # сортируем список по второму элементу кортежей
        result.sort(key=lambda x: x[1])
        result.reverse()  # реверс списка, чтобы вначале был максимальный индекс

        for i in result:
            print(i[0], ':', i[1])

        print('Получено всего статей ', len(result))

    finally:
        sleep(5)
        driver.quit()  # закрываем браузер в любом случае
