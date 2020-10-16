# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import random
import json
import requests
from bs4 import BeautifulSoup
from time import sleep

DOMAIN = 'https://leroymerlin.ru'


def get_html(url):  # получение html кода с абстрактной стр
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


def home_page():  # получение ссылок основных категорий
    url = 'https://leroymerlin.ru/catalogue/'
    category_list = []
    soup = get_html(url)
    main_div = soup.find('nav', class_='leftmenu-small').find('ul')
    li_list = main_div.find_all('li')
    for li in li_list[:-2]:  # последние две ссылки баннеры рекламные
        href = li.find('a').get('href')
        link = DOMAIN + href
        category_list.append(link)
        # print(link)
    # print(category_list)
    return category_list


def category_page(url):  # получение ссылок из категорий/субкатегорий
    x = random.randint(1, 3)
    sleep(x)
    soup = get_html(url)
    link_list = []
    main_list = soup.find_all('uc-catalog-facet-link')
    for el in main_list:
        href = el.find('a').get('href')
        link = DOMAIN + href
        link_list.append(link)  # список линков из категории/субкатегории
        # print(link)
    return link_list


def product_page(url):  # парсинг самой страницы со списком товаров
    data_list = []
    x = random.randint(2, 5)
    sleep(x)  # на всякий случай) можно убрать
    soup = get_html(url)
    # main_div = soup.find('div', attrs={'data-element-id': 'plp-card-list'})
    paginator = soup.find('div', class_='list-paginator')
    if paginator:
        count = paginator.find_all('a')[-2].get('data-page')
        # print(count)
        for i in range(1, int(count)+1):
            result = page(url + f'?sortby=8&page={i}')  # список всех товаров со страницы
            data_list.append(result)  # список всех товаров из субкатегории
    else:
        result = page(url)  # список всех товаров со страницы
        data_list.append(result)  # список всех товаров из субкатегории

    return data_list


def page(url):  # парсинг карточки с товаром
    # data_list = []
    soup = get_html(url)
    product_list = soup.find_all('product-card')
    for item in product_list:
        x = random.randint(3, 5)  # на всякий случай, чтоб не забанили)
        sleep(x)
        title = item.get('product-name')
        # title = item.find('a', slot='picture').get('title')
        category = item.get('data-category')
        url = item.get('data-product-url')
        link = DOMAIN + url
        img_list = item.find('img', class_='plp-item-picture__image').get('src')  # получаем список из двух ссылок на картинки
        img = img_list.split(' ')[0]  # разделяем по пробелу и берем первую
        # data = (title, category, link, img)
        data = {
            'title': title,
            'category': category,
            'link': link,
            'img': img
        }
        print(data)
        # for i in data:  # запись результатов в txt
        #     with open('result_leroymerlin.txt', 'a', encoding='utf-8') as file:
        #         file.write(i)

        with open('res_leroymerlin.json', 'a', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    # return data_list  # список всех товаров со страницы


def main():
    subcat_list, subsubcat_list = [], []
    category_list = home_page()  # получили список ссылок категорий
    print(f'всех категорий {len(category_list)}')  # для проверки правильности парсинга, можно закомментировать
    # print(category_list)

    for cat in category_list:
        subcat = category_page(cat)  # список ссылок подкатегорий
        subcat_list.append(subcat)
    # print(len(subcat_list))  # получили список списков
    # print(*subcat_list)
    for llist in subcat_list:  # из списка списков берем список ссылок
        for num in llist:  # из списка берем каждую ссылку
            result = product_page(num)  # получаем список товаров со стр
            print(f'парсим {num}')  # добавлено для наглядности работы парсера


main()
