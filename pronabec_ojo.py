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

driver = webdriver.Chrome()

email = 'diegotocre@gmail.com'
pw = 'pronabec'

driver.get('https://ecoid.pe/login/r2tbzg902jxaq6c0tmc2zr6txgzfzmiy/?path=/buscar/&shown=0&reference=https://ojo.pe/buscar/?q=pronabec')
driver.find_element_by_xpath('//*[@name="email"]').send_keys(email)
driver.find_element_by_xpath('//*[@id="pass1"]').send_keys(pw)
driver.find_element_by_xpath('/html/body/div/div[2]/div/section/form/div[3]/input').click()

driver.get("https://ojo.pe/buscar/?q=pronabec")

data = []

writer = codecs.open('ojo.csv', 'w', "utf-8-sig")

pags = 1

for j in range(pags):

    count = len(driver.find_elements_by_xpath('/html/body/div[6]/main/div/div[4]/article'))
    print(count)
    for i in range(1, count + 1):
        print(i)
        driver.implicitly_wait(15)
        time.sleep(3)

        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/main/div/div[4]/article[{0}]/div/h2/a'.format(i))))
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/main/div/div[4]/article[{0}]/div/h2/a'.format(i))))

        boton1 = driver.find_element_by_xpath('/html/body/div[6]/main/div/div[4]/article[{0}]/div/h2/a'.format(i))
        driver.execute_script("arguments[0].click();", boton1)

        driver.implicitly_wait(15)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//h1[@class="news-title " | @class="news-title"]')))

        #Titulo, resumen y fecha
        titulo = driver.find_element_by_xpath('//h1[@class="main-title"]').text
        print(titulo)
        try:
            summary = driver.find_element_by_xpath('/html/body/div[6]/main/div/article/div/div[5]/h2').text
            print(summary)
        except NoSuchElementException:
            summary = ''
            print(summary)
        date = driver.find_element_by_xpath('/html/body/div[6]/main/div/article/div/div[1]/div[@class="fecha"]').text
        print(date)

        # Contenido completo
        content = driver.find_elements_by_xpath('/html/body/div[6]/main/div/article/div/div[5]/div/p')
        text_content = []
        for i in range(len(content)):
            text_content.append(content[i].text)
        all_content = ' '.join(text_content)
        if not content:
            content = driver.find_element_by_xpath('/html/body/div[6]/main/div/article/div/div[5]/div').text
            all_content = content

        link = driver.current_url

        data.append((titulo, summary, date, all_content, link))

        df = pd.DataFrame(data, columns=["Titulo", "Resumen", "Fecha", "Contenido", "Link"])
        df.to_csv('ojo.csv', index=False, encoding='utf-8-sig')

        # writer.write(titulo, summary, date, all_content,'\n')

        driver.execute_script("window.history.go(-1)")

    g = j + 2
    if j != pags - 1:
        ano = "2018"
        mes = "05"
        dia = "25"
        driver.implicitly_wait(15)
        driver.get('https://elcomercio.pe/buscar/?query=pronabec&category=elcomercio&sort=desc&type=&from=' + ano + '-' + mes + '-' + dia + '&until=' + ano + '-' + mes + '-' + dia + '&page=' + str(g))
        print(g)

driver.quit()