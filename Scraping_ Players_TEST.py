# Definindo os framewroks e Librarys usadas

import time
import requests
import pandas as pd
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Definindo as Variaveis de ambiente
ROOT_FOLDER = Path(__file__).parent
ROOT_FILE = ROOT_FOLDER / 'chromedriver.exe'
ROOT_CHROME_DRIVER = str(ROOT_FILE)

""" DEFININDO AS CONSTANTS DO SCRAPING"""
URL_MAIN = str('https://www.premierleague.com/stats/top/players/')
VARS_URLS = ['appearances']
# VARS_URLS = ['appearances', 'goal_assist', 'goals',
#              'clean_sheet', 'mins_played']
XPATH_COOKIES = '//button[@id="onetrust-accept-btn-handler"]'
XPATH_ADVERTS = '//a[@id="advertClose"]'
XPATH_FILTER_SEASONS = '//div[@data-dropdown-block="FOOTBALL_COMPSEASON"]'
XPATH_ALL_SEASONS = '//li[@data-option-name="All Seasons"]'
XPATH_DATA = '//tbody[@class="stats-table__container statsTableContainer"]'
XPATH_NEXT_PAGE = '//div[@class="paginationBtn paginationNextContainer"]'
XPATH_PLAYER_INFO = '//a[@class="playerName"]'
XPATH_IMAGE = '//img[@class="img"]'
ACTUAL_URL = ''
FIND_ROW = []
FIND_IMAGE = []
LISTA_DADOS = []
LISTA_URL = []
CONT = 0

''' CONFIGURANDO AS DEFINIÇÕES DE ACESSOS HTTP'''

# Configurando as conexões de serviço
service = Service(executable_path=ROOT_CHROME_DRIVER)

# Configurando as options do webdriver
options = Options()
options.add_argument('window-size=1920,1080')

# Configurando o browser e URL de Acesso
browser = webdriver.Chrome(service=service, options=options)
browser.get(URL_MAIN)
sleep(1)


'''  DEFININDO AS FUNÇÕES DO CODIGO '''


def check_element_presence(Xpath: str):
    try:
        WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.XPATH, Xpath))
        )

        return True

    except Exception:
        return False


def check_element_is_visible(Xpath: str):
    try:
        WebDriverWait(browser, 1).until(
            EC.visibility_of_element_located((By.XPATH, Xpath))
        )

        return True

    except Exception:
        return False


# Definindo uma função que fecha um determinado botão na content
def click_btn_content(Xpath: str):
    # Clicando no botão correspondente a aceitar os cokkies de navegação
    browser.switch_to.default_content()
    button_content = browser.find_element(By.XPATH, Xpath)
    button_content.click()
    print('Botão Cokkies fechado...Ok')

    return None


# Definindo uma função que fecha um determinado botão na window
def click_btn_window(Xpath: str):
    btn_window = browser.find_element(By. XPATH, Xpath)
    btn_window.click()
    return None


# Definindo a Função que extrai os dados de cada tabela
def return_rows(list_data: list, Xpath_data: str, Find: list):
    elemetos_1 = browser.find_elements(By.XPATH, Xpath_data)
    for rows in elemetos_1:
        Find = rows.text.split('\n')
        list_data.append(Find)
    return list_data


# Definindo a função que retorna o link da URL dos Escudos
def return_Image(list_url: list, Xpath_player_info: str, Xpath_image: str):
    elementos = browser.find_elements(By.XPATH, Xpath_player_info)
    for elemento in elementos:
        link_club = elemento.get_attribute('href')
        link_text = str(link_club).strip()

        browser.get(link_text)
        sleep(1)

        player_image = browser.find_element(By.XPATH, Xpath_image)
        player_image_src = player_image.get_attribute("src")
        list_url.append(player_image_src)

        browser.back()
        sleep(1)
        continue
    return list_url


# Definindo a Função que salva os dados no excel
def save_to_excel(list_dados: list, list_url: list):
    planilha = []
    for lista_interna in list_dados:
        # Dividir a lista interna em partes de 5 elementos
        partes = [lista_interna[i:i+5] for i in range(0, len(lista_interna), 5)]

        # Adicionar cada parte como uma linha na planilha
        planilha.extend(partes)
    df_dados = pd.DataFrame(planilha)

    planilha2 = []
    planilha2.extend(list_url)
    df_urls = pd.DataFrame(planilha2)

    df_merged = pd.concat([df_dados, df_urls], axis=1)

    df_merged.to_excel(f'Players_{url}_url.xlsx', index=False)

    return None


hora_inicio = time.time()
print("INICIO DA EXECUÇÃO EM:", hora_inicio)

click_btn_content(XPATH_COOKIES)
sleep(1)


for index, url in enumerate(VARS_URLS):

    # Acessando a nova página
    print(f'Acessando a página de {url}.....Ok')

    ACTUAL_URL = URL_MAIN+url
    browser.get(ACTUAL_URL)
    sleep(1)

    ''' ENCONTRANDO OS BOTÕES PARA EXECUTAR A PAGINA '''

    # Fechando o botão de anuncio se existir
    if check_element_is_visible(XPATH_ADVERTS):
        click_btn_window(XPATH_ADVERTS)
        sleep(1)
        print('Botão de Advert Click....Ok')
    else:
        print('Botão Advert passed....Ok')
        pass

    # Clicando no botão de filtro das temporadas
    click_btn_window(XPATH_FILTER_SEASONS)
    sleep(1)
    print('Botão de Filter...Ok')

    # Clicando no botão de todas as temporadas
    click_btn_window(XPATH_ALL_SEASONS)
    sleep(1)
    print('Botão de All Seasons...Ok')

    # Loop While que percorre as paginas e chama a função de extração
    while True:

        try:
            CONT += 1
            sleep(1.5)
            print(f'Extraindo Dados de {url}.....PG-{CONT}')
            return_rows(LISTA_DADOS, XPATH_DATA, FIND_ROW)
            print(f'Extraindo URLs de {url}.....PG-{CONT}')
            return_Image(LISTA_URL, XPATH_PLAYER_INFO, XPATH_IMAGE)
            print('Proxima Tabela....')
            click_btn_window(XPATH_NEXT_PAGE)
            sleep(1.5)

            if check_element_is_visible(XPATH_NEXT_PAGE):
                print('Next Button..Ok')

            else:
                print('Next Button Missed...Ok')
                raise Exception

        except Exception:
            CONT += 1
            sleep(1.5)
            print(f'Extraindo Ultimos Dados de {url}.....PG-{CONT}')
            return_rows(LISTA_DADOS, XPATH_DATA, FIND_ROW)
            print(f'Extraindo Ultimas URLs de {url}.....PG-{CONT}')
            return_Image(LISTA_URL, XPATH_PLAYER_INFO, XPATH_IMAGE)
            print('Exception Passed, Move to Saving...')
            break
    CONT = 0
    # invocando a função que salva os dados na planilha
    print('Salvando dados no Excel....')
    save_to_excel(LISTA_DADOS, LISTA_URL)

    print(f'Dados Salvos em: Players_{url}_url.xlsx')

    # Mensagens de Finalização
    print(f'SCRAPING DE {url} FINALIZADO')
    print('Mudando de Janela....')
    LISTA_DADOS = []
    LISTA_URL = []

print('Ultima Janela Colect....Ok')
hora_final = time.time()
temp_exec = hora_final - hora_inicio
temp_exec_format = time.strftime("%H:%M:%S", time.gmtime(temp_exec))

print("O código terminou em:", hora_final)
print("Tempo de execução:", temp_exec_format)
print('SCRAPING COMPLETO')
