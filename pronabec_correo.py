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
from selenium.common.exceptions import NoSuchElementException
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)

email = 'diegotocre@gmail.com'
pw = 'pronabec'

driver.get('https://ecoid.pe/login/547a1802dfdcaa443d08c92c8dac62e9/?path=/buscar/&shown=0&reference=https://diariocorreo.pe/buscar/?q=pronabec')
driver.find_element_by_xpath('//*[@name="email"]').send_keys(email)
driver.find_element_by_xpath('//*[@id="pass1"]').send_keys(pw)
driver.find_element_by_xpath('/html/body/div/div[2]/div/section/form/div[3]/input').click()

driver.get('https://diariocorreo.pe/buscar/?page=1&q=pronabec')

data = []

writer = codecs.open('correo.csv', 'w', "utf-8-sig")

pags = 6

for j in range(pags):

    count = len(driver.find_elements_by_xpath('//article[@class="article-section"]'))
    print(count)
    for i in range(1, count + 1):
        print(i)
        driver.implicitly_wait(15)
        time.sleep(3)

        boton1 = driver.find_element_by_xpath('//main/div[4]/section[2]/div[1]/article[@class="article-section"][{0}]/div/h3/a'.format(i))
        driver.execute_script("arguments[0].click();", boton1)

        driver.implicitly_wait(15)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="idreveal"]/main/div[3]/article/div/h1')))

        #Titulo, resumen y fecha
        titulo = driver.find_element_by_xpath('//*[@id="idreveal"]/main/div[3]/article/div/h1').text
        print(titulo)
        try:
            summary = driver.find_element_by_xpath('//*[@id="idreveal"]/main/div[3]/article/div/strong').text
            print(summary)
        except NoSuchElementException:
            summary = ''
            print(summary)
        try:
            date = driver.find_element_by_xpath('//*[@id="idreveal"]/main/div[3]/article/div/div[2]/p/strong').text
        except NoSuchElementException:
            date = driver.find_element_by_xpath('//*[@id="idreveal"]/main/div[3]/article/div/div[1]/p').text
        print(date)

        # Contenido completo
        content = driver.find_elements_by_xpath('//*[@id="idreveal"]/main/div[3]/article/div/div[6]/p')
        text_content = []
        for i in range(len(content)):
            text_content.append(content[i].text)
        all_content = ' '.join(text_content)
        if not content:
            content = driver.find_elements_by_xpath('//*[@id="idreveal"]/main/div[3]/article/div/div[7]/p')
            text_content = []
            for i in range(len(content)):
                text_content.append(content[i].text)
            all_content = ' '.join(text_content)

        link = driver.current_url

        data.append((titulo, summary, date, all_content, link))

        df = pd.DataFrame(data, columns=["Titulo", "Resumen", "Fecha", "Contenido", "Link"])
        df.to_csv('correo.csv', index=False, encoding='utf-8-sig')

        # writer.write(titulo, summary, date, all_content,'\n')

        driver.execute_script("window.history.go(-1)")

    g = j + 2
    if j != pags - 1:
        ano = "2018"
        mes = "05"
        dia = "28"
        driver.implicitly_wait(15)
        driver.get('https://diariocorreo.pe/buscar/?page=' + str(g) +'&q=pronabec')
        print(g)

driver.quit()