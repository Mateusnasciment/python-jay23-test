import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests

# Configurando o navegador
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)

driver.get('https://www.truepeoplesearch.com/')

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

API_KEY = 'YOUR_API_KEY_HERE'
SITE_KEY = 'SITE_KEY_HERE'
URL = 'https://www.truepeoplesearch.com/'

def solve_captcha(site_key, url, api_key):
    captcha_id = requests.post(f'https://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={site_key}&pageurl={url}').text.split('|')[1]
    time.sleep(10)
    response = requests.get(f'https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}').text
    while 'CAPCHA_NOT_READY' in response:
        time.sleep(5)
        response = requests.get(f'https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}').text
    captcha_response = response.split('|')[1]
    return captcha_response

with open('Memphis-recently-sold-feb-21-2023_-_Memphis-recently-sold-feb-21-2023_4.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        search_bar = driver.find_element_by_xpath('//*[@id="searchBar"]')
        search_bar.clear()
        search_bar.send_keys(row[0])
        search_bar.send_keys(Keys.RETURN)
        time.sleep(5)

        site_key = driver.find_element_by_xpath('//div[@class="g-recaptcha"]/@data-sitekey')
        captcha_response = solve_captcha(site_key, URL, API_KEY)

        driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{captcha_response}";')

        verify_button = driver.find_element_by_xpath('//button[@class="btn btn-primary btn-lg js-verify js-scroll"]')
        verify_button.click()
        time.sleep(5)

        resultados = driver.find_elements_by_xpath('//div[@class="infoBox"]')
        for resultado in resultados:
            nome = resultado.find_element_by_xpath('.//div[@class="name"]//span').text
            endereco = resultado.find_element_by_xpath('.//div[contains(text(),"Address:")]/span').text
            telefone = resultado.find_element_by_xpath('.//div[contains(text(),"Phone:")]/span').text
            email = resultado.find_element_by_xpath('.//div[contains(text(),"Email:")]/span').text
