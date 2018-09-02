import json
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.webscraper.io/'

url = BASE_URL + 'test-sites/e-commerce/static/computers/laptops'


def get_dom(url):
    res = requests.get(url)
    dom = BeautifulSoup(res.text, 'lxml')
    return dom


def get_product(product, category):
    image = product.select_one('.img-responsive')
    title = product.select_one('.title')
    price = product.select_one('.pull-right.price')
    rating = product.select_one('[data-rating]')
    description = product.select_one('.description')

    price = price.text.replace('$', '')
    title = title.get('title')

    if category == '' or title == '':
        print(category, title)
        return {}

    return {
        'category': category,
        'title': title,
        'image': BASE_URL + image.get('src', '/#'),
        'price': float(price),
        'rating': int(rating.get('data-rating', 0)),
        'description': description.text
    }


def get_category(dom):
    category = dom.select_one('.page-header')
    return category.text if category != None else ''


def get_products(dom, result):
    products = dom.select('.thumbnail')
    category = get_category(dom)

    while True:
        for product in products:
            p = get_product(product, category)
            if p != {}:
                result.append(p)

        if can_paginate(dom):
            next_url = dom.select_one('[rel=next]')
            next_url = next_url.get('href', '')
            dom = get_dom(next_url)
            category = get_category(dom)
            products = dom.select('.thumbnail')
        else:
            return result


def can_paginate(dom):
    return dom.select_one('[rel=next]') != None


def run(dom):
    result = []
    categories = dom.select('#side-menu a')

    for category in categories:
        url = BASE_URL + category.get('href', '')
        dom = get_dom(url)
        get_products(dom, result)

        subcategories = dom.select('.subcategory-link')
        if subcategories:
            for subcategory in subcategories:
                url = BASE_URL + subcategory.get('href', '')
                dom = get_dom(url)
                get_products(dom, result)

    return result


def can_paginate_eigon(dom):
    next_url = dom.select_one('[rel=next]')
    return (next_url != None, next_url.get('href', ''))

dom = get_dom(url)
result = run(dom)

arquivo = open('ecommerce.json', 'w')
arquivo.write(json.dumps(result, indent=2))
arquivo.close()
