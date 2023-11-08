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
VARS_URLS = ['goals', 'goal_assist',
             'clean_sheet', 'appearances', 'mins_played']
XPATH_COOKIES = '//button[@id="onetrust-accept-btn-handler"]'
XPATH_ADVERTS = '//a[@id="advertClose"]'
XPATH_FILTER_SEASONS = '//div[@data-dropdown-block="FOOTBALL_COMPSEASON"]'
XPATH_ALL_SEASONS = '//li[@data-option-name="All Seasons"]'
XPATH_DATA = '//tbody[@class="stats-table__container statsTableContainer"]'
XPATH_NEXT_PAGE = '//div[@class="paginationBtn paginationNextContainer"]'
XPATH_PLAYER_INFO = '//a[@class="playerName"]'
ACTUAL_URL = ''
FIND_ROW = []
LISTA_DADOS = []
LISTA_DADOS_2 = []
LISTA_COMPLETA = []

CONT = 0

''' CONFIGURANDO AS DEFINIÇÕES DE ACESSOS HTTP'''

# Configurando as conexões de serviço
service = Service(executable_path=ROOT_CHROME_DRIVER)

# Configurando as options do webdriver
options = Options()
options.add_argument('window-size=1920,1080')

# Configurando o browser e URL de Acesso
browser = webdriver.Chrome(service=service, options=options)
browser.get(URL_MAIN+VARS_URLS[0])
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
def return_rows(list_data: list, Xpath_data: str, Xpath_Player_Info: str, Find: list, list_data_2: list, list_complete: list):
    elemetos_1 = browser.find_elements(By.XPATH, Xpath_data)
    for rows in elemetos_1:
        Find = rows.text.split('\n')
        list_data.append(Find)

    elementos = browser.find_elements(By.XPATH, Xpath_Player_Info)
    for elemento in elementos:
        # list_age = []
        # list_country = []
        # list_url = []

        link_club = elemento.get_attribute('href')
        link_text = str(link_club).strip()

        response = requests.get(link_text)
        page_content = response.text

        soup = BeautifulSoup(page_content, 'html.parser')
        url_player = soup.find('img', {'class': 'img'})
        info_players = soup.findAll('div', {'class': 'player-info__info'})

        if url_player:
            picture_player = url_player.get('src')
            list_data_2.append(picture_player)
            pass
        if info_players:
            for ages in info_players:
                for age in ages:
                    info = age.text.replace('\n', '').replace(' ', '').splitlines(True)
                    for list_info in info:
                        list_data_2.append(list_info)

            list_complete = list_data + list_data_2

    return list_complete


# Definindo a Função que salva os dados no excel
def save_to_excel(list_complete: list):
    planilha = []
    for lista_interna in list_complete:
        partes = [lista_interna[i:i+10] for i in range(0, len(lista_interna), 10)]
        planilha.extend(partes)

    df_final = pd.DataFrame(planilha)

    df_final.to_excel(f'Teste_{VARS_URLS[0]}_url.xlsx', index=False)

    return None


hora_inicio = time.time()
print("INICIO DA EXECUÇÃO EM:", hora_inicio)

click_btn_content(XPATH_COOKIES)
sleep(1)

# Acessando a nova página
print(f'Acessando a página de {VARS_URLS[0]}.....Ok')

ACTUAL_URL = URL_MAIN+VARS_URLS[0]
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

try:
    CONT += 1
    sleep(1)
    print(f'Extraindo Dados de {VARS_URLS[0]}.....PG-{CONT}')
    return_rows(LISTA_DADOS, XPATH_DATA, XPATH_PLAYER_INFO, FIND_ROW, LISTA_DADOS_2, LISTA_COMPLETA)
    print(f'Extraindo URLs de {VARS_URLS[0]}.....PG-{CONT}')
    print('Proxima Tabela....')
    click_btn_window(XPATH_NEXT_PAGE)
    sleep(1)

    if check_element_is_visible(XPATH_NEXT_PAGE):
        print('Next Button..Ok')
        pass

    else:
        print('Next Button Missed...Ok')
        raise Exception

except Exception:
    CONT += 1
    print(f'Extraindo Ultimos Dados de {VARS_URLS[0]}.....PG-{CONT}')
    return_rows(LISTA_DADOS, XPATH_DATA, XPATH_PLAYER_INFO, FIND_ROW, LISTA_DADOS_2, LISTA_COMPLETA)
    print(f'Extraindo Ultimas URLs de {VARS_URLS[0]}.....PG-{CONT}')
    print('Exception Passed, Move to Saving...')

# invocando a função que salva os dados na planilha
print('Salvando dados no Excel....')
# save_to_excel(LISTA_COMPLETA)
print(LISTA_COMPLETA)

print(f'Dados Salvos em: Players_{VARS_URLS[0]}_url.xlsx')

# Mensagens de Finalização
print(f'SCRAPING DE {VARS_URLS[0]} FINALIZADO')
print('Mudando de Janela....')
LISTA_DADOS = []
LISTA_DADOS_2 = []
LISTA_COMPLETA = []

print('Ultima Janela Colect....Ok')
hora_final = time.time()
temp_exec = hora_final - hora_inicio
temp_exec_format = time.strftime("%H:%M:%S", time.gmtime(temp_exec))

print("O código terminou em:", hora_final)
print("Tempo de execução:", temp_exec_format)
print('SCRAPING COMPLETO')
