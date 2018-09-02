import requests
from bs4 import BeautifulSoup

url = 'https://www.webscraper.io/test-sites/tables'


def get_dom(url):
    res = requests.get(url)
    dom = BeautifulSoup(res.text, 'lxml')
    return dom


def get_data(dom, replace=True):
    data = []
    tables = dom.select('table')

    for table in tables:
        rows = table.select('tr')
        for row in rows:
            line = list(row.stripped_strings)
            line = line[1:]

            if len(line) < 3:
                continue

            if replace == False:
                if ','.join('-' * len(line)) == ','.join(line):
                    continue
            else:
                for index in range(len(line)):
                    if line[index] == '-':
                        line[index] = 'N/A'

            data.append(line)

    return data


def save_data(data):
    csv = open('table.csv', 'w')

    for line in data:
        csv_line = ','.join(line)
        csv.write(csv_line + '\n')
    
    csv.close()

dom = get_dom(url)
data = get_data(dom, False)
save_data(data)
