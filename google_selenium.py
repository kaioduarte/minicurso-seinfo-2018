from selenium import webdriver

# Chrome
driver = webdriver.Chrome()

# Firefox
# driver = webdriver.Firefox()

URL = 'https://www.google.com.br/'

# Navega para a URL especificada
driver.get(URL)

# Acha elemento por id
text_area = driver.find_element_by_id('lst-ib')

pesquisa = input('Digite seu termo de busca: ')

# Envia conteúdo para input
text_area.send_keys(pesquisa)

# Acha 'botão'
botao = driver.find_element_by_css_selector('[name=btnK]')

# Envia formulário
botao.submit()

# Fecha browser
driver.close()
