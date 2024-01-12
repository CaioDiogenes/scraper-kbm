import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

SITE_URL = 'https://www.kabum.com.br'
TERMO_PESQUISA = 'SSD'
NUM_PAGS = 1
NOME_ARQUIVO = "{}_{}.csv".format(TERMO_PESQUISA, datetime.datetime.now().strftime("%d%m%Y%H%M"))

print(f"[Info] Starting")

def extrair_infos_produto(produto):
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'priceCard')))
    titulo = produto.find('span', class_='nameCard').text
    preco_a_vista = float(produto.find('span', class_='priceCard').text.split('R$')[1].replace('.', '').replace(',', '.'))
    avaliacao = len(produto.find_all('div', class_='estrelaAvaliacao'))
    qtde_avaliacao = int(produto.find('div', class_='labelTotalAvaliacoes').text[1:-1]) if produto.find('div', class_='labelTotalAvaliacoes') else 0
    link_produto = produto.find('a', class_='productLink').get('href')
    return titulo, preco_a_vista, avaliacao, qtde_avaliacao, link_produto

browser_options = Options()
browser_options.add_argument('--headless')
# driver = webdriver.Chrome(options=browser_options)
driver = webdriver.Chrome()
driver.get(SITE_URL)

campo_busca = driver.find_element(By.ID, value='input-busca')
campo_busca.send_keys(TERMO_PESQUISA)
campo_busca.send_keys(Keys.ENTER)

titulos = []
precos_a_vista = []
avaliacoes = []
qtde_avaliacoes = []
link = []

p = 1
while p <= NUM_PAGS:
    try:
        print(f"[Info] Reading page {p}...")

        wait = WebDriverWait(driver, 10)

        try:
            html = driver.find_elements(By.TAG_NAME, 'main')[0]
        except IndexError as ie:
            driver.refresh()
            continue

        html = html.get_attribute("innerHTML")

        sopa = BeautifulSoup(html, 'html.parser')
        
        for item in sopa.find_all('div', {'class': 'productCard'}):
            titulo, preco_a_vista, avaliacao, qtde_avaliacao, link_produto = extrair_infos_produto(item)
        
            titulos.append(titulo)
            precos_a_vista.append(preco_a_vista)
            avaliacoes.append(avaliacao)
            qtde_avaliacoes.append(qtde_avaliacao)
            link.append( f'{SITE_URL}{link_produto}')
            
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'nextLink'))).click()
        
        p += 1

        if p > NUM_PAGS:
            print("[Info] Extração concluída.")
            break
    except Exception as e:
        print("[Error] Exceção:", e)
        break

driver.close()

df = pd.DataFrame()
df["Link Produto"] = link
df["Nome"] = titulos
df["Preco_a_vista"] = precos_a_vista
df["Avaliacao"] = avaliacoes
df["Qtde_Avaliacoes"] = qtde_avaliacoes

print(f"\n[Done] {len(df)} registros adicionados.")

df.to_csv(NOME_ARQUIVO, index=False)
print(f"[Info] Arquivo salvo como {NOME_ARQUIVO}.")