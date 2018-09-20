import requests
from bs4 import BeautifulSoup
from itertools import product


headers = { 'User-Agent': 'Mozilla/5.0' }
url = 'http://tabnet.datasus.gov.br/cgi/{}.exe?ibge/cnv/aagpr.def'

tipo = {
    'main': 'deftohtm',
    'pesquisa': 'tabcgi'
}

default_payload = [
    ('formato', 'prn'), # csv
    ('mostre', 'Mostra'),
]

def get_selects(dom: BeautifulSoup) -> list:
    selects = []

    for s in dom.select('select'):
        if s.option:
            selects.append(s)
    
    return selects


def get_selects_names(selects: list) -> list:
    names = []

    for s in selects:
        names.append(s.get('name'))

    return names


def get_selects_values(selects: list) -> list:
    selects_values = []
    
    for s in selects:
        values = []
        for option in s.select('option'):
            values.append(option.get('value'))
        selects_values.append(values)

    return selects_values


def get_query_parameter(payload: list) -> str:
    query_elements = []

    for name, value in payload:
        query_elements.append(name + '=' + value)

    return '&'.join(query_elements)


def save_file(filename: str, content: str):
    with open(filename, 'w') as file:
        file.write(content)


if __name__ == '__main__':
    res = requests.get(url.format(tipo['main']), headers=headers)
    dom = BeautifulSoup(res.text, 'html.parser')

    selects = get_selects(dom)
    selects_names = get_selects_names(selects)
    selects_values = get_selects_values(selects)

    for index, data in enumerate(product(*selects_values)):
        payload = default_payload + list(zip(selects_names, data))
        data = get_query_parameter(payload)

        _res = requests.post(url.format(tipo['pesquisa']), headers=headers, data=data)
        _dom = BeautifulSoup(_res.text, 'lxml')

        if _dom.find(text='Nenhum registro selecionado'):
            continue
        else:
            content = _dom.pre.text.strip().splitlines()[:-1]
            save_file('{}.csv'.format(index), '\n'.join(content))

            for el in ['.Escondido', '.testeira > .testeira', '.rodape_htm', 'pre', 'br']:
                to_remove = _dom.select_one(el)
                to_remove.decompose()

            metadata_content = list(_dom.select_one('.testeira').stripped_strings)

        save_file('{}-metadata.txt'.format(index), '\n'.join(metadata_content))
                
