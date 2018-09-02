from time import sleep
from selenium import webdriver

options = webdriver.ChromeOptions()
profile = {
    "plugins.plugins_list": [{
		"enabled": False,
		"name":"Chrome PDF Viewer"
	}],
    "download.default_directory" : "/home/kds/"
}
options.add_experimental_option("prefs", profile)
driver = webdriver.Chrome(chrome_options=options)

URL = 'http://moodle.utfpr.edu.br/'


def login(driver):
    username = input('login: ')
    password = input('senha: ')

    username_input = driver.find_element_by_id('username')
    password_input = driver.find_element_by_id('password')

    username_input.send_keys(username)
    password_input.send_keys(password)

    username_input.submit()


def get_disciplines_url(driver):
    sleep(2)
    links = driver.find_elements_by_css_selector('.type_system .type_course > p > a')

    hrefs = set()
    for link in links:
        hrefs.add(link.get_property('href'))

    return list(hrefs)


def get_pdfs(driver):
    disciplines_url = get_disciplines_url(driver)
    css = 'li.activity.resource .activityinstance > a'
    
    for discipline in disciplines_url:
        driver.get(discipline)

        activities = driver.find_elements_by_css_selector(css)
        for activity in activities:
            img = activity.find_element_by_tag_name('img')
            src = img.get_property('src')

            src_splitted = src.split('/')

            if src_splitted[-1] == 'pdf-24':
                activity.click()


driver.get(URL)
login(driver)
get_pdfs(driver)