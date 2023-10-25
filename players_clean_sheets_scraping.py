# Definindo os framewroks e Librarys usadas
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
import pandas as pd

# Definindo as Variaveis de ambiente
ROOT_FOLDER = Path(__file__).parent
ROOT_FILE = ROOT_FOLDER / 'chromedriver.exe'
ROOT_CHROME_DRIVER = str(ROOT_FILE)
VALUE_INT = ''
LISTA_DADOS = []
FIND = []

""" DEFININDO AS URL's DO SCRAPING"""
URL_MAIN = 'https://www.premierleague.com/stats/top/players/'
VARS_URLS = ['goals', 'goal_assist', 'clean_sheet', 'appearances', 'mins_played']

''' CONFIGURANDO AS DEFINIÇÕES DE ACESSOS HTTP'''

# Configurando as conexões de serviço
service = Service(executable_path=ROOT_CHROME_DRIVER)

# Configurando as options do webdriver
options = Options()
options.add_argument('window-size=1080,1920')

# Configurando o browser e URL de Acesso
browser = webdriver.Chrome(service=service, options=options)

# Iterando sobre o programa para usar varias URL's

browser.get(URL_MAIN+VARS_URLS[2])

''' ENCONTRANDO OS BOTÕES PARA FILTRAR A PAGINA '''

# Tempo de Espera para carregar os elementos da pagina
sleep(2)

# Encontrando o botão de filtro das temporadas
filter_seasons = browser.find_element(
    By.XPATH, '//div[@data-dropdown-block="FOOTBALL_COMPSEASON"]')
filter_seasons.click()
sleep(2)

# Selecionando o botão de todas as temporadas
all_seasons = browser.find_element(
    By.XPATH, '//li[@data-option-name="All Seasons"]')
all_seasons.click()
sleep(2)

# Encontrando o valor do botão que aciona a proxima pagina
next_page_button = browser.find_element(
    By.XPATH, '//div[@class="paginationBtn paginationNextContainer"]')


# Função que extrai os dados de cada tabela
def return_rows(list_data: list):
    elemento = browser.find_elements(By.XPATH, "//tbody \
                        [@class='stats-table__container statsTableContainer']")
    for elementos in elemento:
        FIND = elementos.text.split('\n')
        list_data.append(FIND)
    return list_data


# Função que salva os dados no excel
def save_to_excel(list: list):
    planilha = []

    for lista_interna in list:
        # Dividir a lista interna em partes de 5 elementos
        partes = [lista_interna[i:i+5] for i in range(0, len(lista_interna), 5)]

        # Adicionar cada parte como uma linha na planilha
        planilha.extend(partes)

    df = pd.DataFrame(planilha)
    df.to_excel(f'{VARS_URLS[2]}.xlsx', index=False)

    return None


# Loop While que percorre as paginas e chama a função de extração
while True:

    try:
        return_rows(LISTA_DADOS)
        next_page_button.click()

        if WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class=\
                                "paginationBtn paginationNextContainer"]'))
        ):
            continue
        else:
            print('No Presence of Button')
            break

    except Exception:
        print('Exception Failed')
        break

# Finalizando a sessão Webdriver e fechando o navegador
sleep(1)
browser.quit()

# invocando a função que salva os dados na planilha
save_to_excel(LISTA_DADOS)

print(f'SCRAPING DE {VARS_URLS[2]} FINALIZADO')
print('SCRAPING COMPLETO')
