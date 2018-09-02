from json import dumps
from argparse import ArgumentParser
from multiprocessing.dummy import Pool

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://github.com'


def get_dom(url: str) -> BeautifulSoup:
    response = requests.get(url)
    dom = BeautifulSoup(response.text, 'lxml')

    return dom


def get_href(anchors: list) -> list:
    hrefs = []

    for anchor in anchors:
        hrefs.append(anchor['href'])

    return hrefs


def search(term: str, page: str = '', total_pages: bool = False) -> tuple:
    dom = get_dom(f'{BASE_URL}/search?q={term}&p={page}&type=Repositories')

    repo_links = get_href(dom.select('.repo-list a.v-align-middle'))

    total_pages_tag = dom.select_one('[data-total-pages]')
    total_pages = int(total_pages_tag['data-total-pages'])

    return repo_links, total_pages if total_pages else (repo_links, )


def get_stripped_text(dom: BeautifulSoup, css: str, many: bool = False):
    selector = dom.select if many else dom.select_one
    target = selector(css)

    if many:
        result = []

        for element in target:
            text = element.text.strip()
            if text:
                result.append(text)

        return result

    return target.text.strip()


def clear_empty_elements(list_: list) -> list:
    cleared_list = []

    for element in list_:
        stripped = element.strip()
        if stripped:
            cleared_list.append(stripped)

    return cleared_list


def get_infos(tags: list, keys: dict) -> dict:
    infos = {}

    for tag in tags:
        if not tag:
           continue

        key, value = clear_empty_elements(tag.text.splitlines())
        infos[keys[key]] = int(value.replace(',', ''))

    return infos


def get_social_infos(dom: BeautifulSoup) -> dict:
    keys = {'Star': 'stars', 'Watch': 'watchers', 'Fork': 'forks'}
    tags = dom.select('.pagehead-actions > li')

    return get_infos(tags, keys)


def get_nav_infos(dom: BeautifulSoup) -> dict:
    keys = {'Issues': 'issues', 'Pull requests': 'pull_requests'}
    tags = [dom.select_one('[data-selected-links^=repo_issues]'),
            dom.select_one('[data-selected-links^=repo_pull]')]

    return get_infos(tags, keys)


def get_link_and_name(dom: BeautifulSoup) -> tuple:
    tag = dom.select_one('[itemprop=name] a')

    link = tag['href']
    name = tag.text.strip()

    return link, name


def get_repo_info(repo_url: str) -> dict:
    dom = get_dom(BASE_URL + repo_url)

    link, name = get_link_and_name(dom)

    branch_css = '[data-tab-filter=branches] > div > a'
    branches = get_stripped_text(dom, branch_css, True)

    languages = get_stripped_text(dom, '.language-color', True)
    description = get_stripped_text(dom, '[itemprop=about]', True)

    return {
        'name': name,
        'link': link,
        'branches': branches,
        'languages': languages,
        'description': description,
        **get_nav_infos(dom),
        **get_social_infos(dom)
    }


def save_result(result: dict, filename: str = 'result'):
    with open(f'{filename}.json', 'w') as file:
        file.write(dumps(result, indent=2, ensure_ascii=False))


def perform(term: str, filename: str):
    repo_links, total_pages = search(term, total_pages=True)
    result = {'term': term, 'total_pages': total_pages, 'repos': []}

    for page in range(1, total_pages + 1):
        print(page, 'of', total_pages)
        for repo_link in search(term, page)[0]:
            result['repos'].append(get_repo_info(repo_link))

    save_result(result, filename)


def settings() -> ArgumentParser:
    parser = ArgumentParser()

    parser.add_argument('-t', help='Search term', required=True)
    parser.add_argument('--filename', help='Filename of scrape\'s output', default='result')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    '''Limitações: só são exibidos até 1k repos na busca'''

    args = vars(settings())
    term, filename = args['t'], args['filename']
    perform(term, filename)
