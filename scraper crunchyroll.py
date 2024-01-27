import pandas as pd
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

def ExportCsv():
    df = pd.DataFrame()
    df["Link Produto"] = link
    df["Nome"] = titulos

    print(f"\n[Done] {len(df)} registros adicionados.")

    df.to_csv(FILENAME, index=False)
    print(f"[Info] Arquivo salvo como {FILENAME}.")

def ExtrairInfos(anime):
    titulo = anime.text
    link_produto = anime.get('href')
    return titulo, link_produto

print(f"[Info] Starting")

DOMAIN = 'https://www.crunchyroll.com'
SITE = 'https://www.crunchyroll.com/pt-br/search?q='
ANIME = 'death note'
PAGINAS = 1
FILENAME = "{}.csv".format(ANIME)

titulos = []
link = []

browser_options = webdriver.ChromeOptions()
browser_options.add_argument('--headless')
driver = webdriver.Chrome(options=browser_options)
driver.get(f'{SITE}{ANIME}')

pyautogui.sleep(5)

campo_busca = driver.find_elements(By.CLASS_NAME, 'search-show-card--FFXv-')[0]
campo_busca.click()

p = 1
while p <= PAGINAS:
    try:
        print(f"[Info] Reading page {p}...")

        wait = WebDriverWait(driver, 10)
        
        pyautogui.sleep(5)

        try:
            html = driver.find_elements(By.CLASS_NAME, 'card')
        except IndexError as ie:
            driver.refresh()
            continue

        for animepageindex in html:
            index = animepageindex.get_attribute("innerHTML")
            sopa = BeautifulSoup(index, 'html.parser')
            ep = sopa.find_all('a')[-1]
            titulo, link_produto = ExtrairInfos(ep)
            titulos.append(f'{ANIME} {titulo}')
            link.append( f'{DOMAIN}{link_produto}')          
        
        titulos.append(f'{ANIME} {titulo}')
        link.append( f'{DOMAIN}{link_produto}')          
        p += 1

        if p > PAGINAS:
            print("[Info] Extração concluída.")
            break
    except Exception as e:
        print("[Error] Exceção:", e)
        break

driver.close()

ExportCsv()