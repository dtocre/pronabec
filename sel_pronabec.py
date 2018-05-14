# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import codecs
import pandas as pd

driver = webdriver.Chrome()

# driver.find_element_by_xpath('//*[@id="pid-user-info"]/div/a[@data-type="login"]').click()
# driver.find_element_by_xpath('/html/body/div/div[2]/div/section/form/div[1]').send_keys("diegotocre@gmail.com")
# driver.find_element_by_xpath('//*[@id="pass1"]').send_keys("Ds96Ds96")

email = 'diegotocre@gmail.com'
pw = ''

driver.get('https://ecoid.pe/login/a94a8fe5ccb19ba61c4c0873d391e987982fbbd3/?path=/&shown=0&reference=https://elcomercio.pe/')
driver.find_element_by_xpath('//*[@name="email"]').send_keys(email)
driver.find_element_by_xpath('//*[@id="pass1"]').send_keys(pw)
driver.find_element_by_xpath('/html/body/div/div[2]/div/section/form/div[4]/input').click()

driver.get("https://elcomercio.pe/buscar/?query=pronabec")
assert "Resultados de búsqueda para: pronabec | El Comercio Perú" in driver.title

# Aca va un for que englobe lo que esta abajo y que navegue segun las paginas
# para esto se debe contar numero de pestanas
# queda pendiente automatizar numero de paginas y boton Next

data = []

# csv_file = open('elcomercio.csv', 'w', encoding='UTF-8')
#
# writer = csv.writer(csv_file)

writer = codecs.open('elcomercio.csv', 'w', "utf-8-sig")

for j in range(11):

    count = len(driver.find_elements_by_xpath('//*[@id="wrapper"]/div[10]/div[3]/article'))
    print(count)

    for i in range(1, count + 1):
    # for i in range(1, count + 1):
        print(i)
        driver.implicitly_wait(15)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/div[10]/div[3]/article[{0}]/div/h2/a[@class="page-link"]'.format(i))))
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div[10]/div[3]/article[{0}]/div/h2/a[@class="page-link"]'.format(i))))
        # driver.implicitly_wait(4) # seconds
        print(i)

        boton1 = driver.find_element_by_xpath('//*[@id="wrapper"]/div[10]/div[3]/article[{0}]/div/h2/a[@class="page-link"]'.format(i))
        boton1.click()

        # # RECHAZAR ALERTAS
        # try:
        #     WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/a')))
        #     print("alert dismissed")
        #     pop_close = driver.find_element_by_xpath('/html/body/div/div[2]/div/a')
        #     pop_close.click()
        # except TimeoutException:
        #     print("no alert")

        # Aqui va el codigo para extraer texto

        driver.implicitly_wait(15)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//h1[@class="news-title " | @class="news-title"]')))

        #Titulo, resumen y fecha
        titulo = driver.find_element_by_xpath('//h1[@class="news-title " | @class="news-title"]').text
        print(titulo)
        summary = driver.find_element_by_xpath('//h2[@class="news-summary " | @class="news-summary"]').text
        date = driver.find_element_by_xpath('//time[@class="news-date" | @class="news-date "]').text

        # Contenido completo
        content = driver.find_elements_by_xpath('//p[@class="parrafo first-parrafo "]')
        text_content = []
        for i in range(len(content)):
            text_content.append(content[i].text)
        all_content = '\n'.join(text_content)

        data.append((titulo, summary, date, all_content))

        df = pd.DataFrame(data, columns=["Titulo", "Resumen", "Fecha", "Contenido"])
        df.to_csv('elcomercio.csv', index=False, encoding='utf-8-sig')

        # writer.write(titulo, summary, date, all_content,'\n')

        driver.execute_script("window.history.go(-1)")

        # RECHAZAR ALERTAS
        # try:
        #     WebDriverWait(driver, 3).until(EC.alert_is_present())
        #     alert = driver.switch_to.alert
        #     alert.dismiss()
        #     print("alert dismissed")
        # except TimeoutException:
        #     print("no alert")
    g = j + 2
    if j != 11:
        ano = "2018"
        mes = "05"
        dia = "12"
        driver.implicitly_wait(10)
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@rel="next"]/a[contains(@href,"&page=' + str(g) + '")]')))
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[@rel="next"]/a[contains(@href,"&page=' + str(g) + '")]')))
        # next1 = driver.find_element_by_xpath('//div[@class="pagination"]/ul/li/a[contains(@href,"&page=' + str(g) + '")]')
        # next1.click()
        driver.get('https://elcomercio.pe/buscar/?query=pronabec&category=elcomercio&sort=desc&type=&from=' + ano + '-' + mes + '-' + dia + '&until=' + ano + '-' + mes + '-' + dia + '&page=' + str(g))
        print(g)

    # RECHAZAR ALERTAS
    # try:
    #     WebDriverWait(driver, 3).until(EC.alert_is_present())
    #     alert = driver.switch_to.alert
    #     alert.dismiss()
    #     print("alert dismissed")
    # except TimeoutException:
    #     print("no alert")

# csv_file = open('elcomercio.csv', 'a')

# writer = csv.writer(csv_file)
#
# for titulo, summary, date, all_content in data:
#     writer.writerow([titulo, summary, date, all_content])

# pensar en automatizar esto para un numero de paginas variable

# popup = driver.find_element_by_xpath('//div[@class="pip-popup pid-without-shadow window-reiterative pid-loaded"]')
#
# /html/body/div/div[2]/div/a

# try:
#     WebDriverWait(driver, 3).until(EC.alert_is_present(),
#                                    'Timed out waiting for PA creation ' +
#                                    'confirmation popup to appear.')
#     alert = driver.switch_to.alert
#     alert.dismiss()
#     print("alert dismissed")
# except TimeoutException:
#     print("no alert")

# try:
#     popup = driver.find_element_by_xpath('//div[@class="pip-popup pid-without-shadow window-reiterative pid-loaded"]')
#     WebDriverWait(driver, 3).until(EC.alert_is_present(),
#                                'Timed out waiting for PA creation ' +
#                                'confirmation popup to appear.')

#METODO AUXILIAR

# quote_page = 'https://elcomercio.pe/peru/conoce-puedes-financiar-credito-educativo-acuerdo-casa-estudio-noticia-516887'
#
# page = urllib.request.urlopen(quote_page)
#
# soup = BeautifulSoup(page, 'html.parser')
#
# name_box = soup.find_all('p', attrs={'class': 'parrafo first-parrafo '})
#
# name = name_box.text.strip()
#
# print(name)