import requests
from bs4 import BeautifulSoup

url = 'https://pt.wikipedia.org/wiki/Ma%C3%A7%C3%A3'

req = requests.get(url)
dom = BeautifulSoup(req.text, 'lxml')

arquivo = open('scraping.txt', 'a')

# titulo = dom.select_one('h1#firstHeading')
titulo = dom.find('h1', {
    'id': 'firstHeading',
    'class': 'firstHeading' })

print('titulo', titulo.text)
arquivo.write(titulo.text + '\n')

conteudo = dom.select_one('#mw-content-text > div > p')
# pai = dom.find('div', { 'id': 'mw-content-text' })
# filho = pai.find('div')
# conteudo = filho.find('p')

print('conteudo', conteudo.text)
arquivo.write(conteudo.text + '\n')

indices = dom.select('#toc > ul span.toctext')

print('indices')
arquivo.write('indices' + '\n')

for indice in indices:
    print(indice.text)
    arquivo.write(indice.text + '\n')

'''
subtitulo = dom.select_one('.mw-headline')
print('subtitulo', subtitulo.text)

conteudo_subtitulo = subtitulo.parent.find_next_sibling('p')
print('conteudo subtitulo', conteudo_subtitulo.text)
'''

subtitulos = dom.select('.mw-headline')

for subtitulo in subtitulos:
    print('SUBTITULO ->', subtitulo.text)
    arquivo.write(subtitulo.text + '\n')
    conteudo = subtitulo.parent.find_next_sibling('p')
    print('CONTEUDO', conteudo.text)
    arquivo.write(conteudo.text + '\n')

arquivo.close()