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


""" DEFININDO AS URL's DO SCRAPING"""
URL_MAIN = str('https://www.premierleague.com/stats/top/clubs/')
VARS_URLS = ['wins', 'losses', 'goals', 'clean_sheet']
LISTA_DADOS = []
FIND = []

''' CONFIGURANDO AS DEFINIÇÕES DE ACESSOS HTTP'''

# Configurando as conexões de serviço
service = Service(executable_path=ROOT_CHROME_DRIVER)

# Configurando as options do webdriver
options = Options()
options.add_argument('window-size=1080,1920')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
# options.add_argument('---headless')

# Configurando o browser e URL de Acesso
browser = webdriver.Chrome(service=service, options=options)
browser.get(URL_MAIN)
sleep(1)

# Econtrando o botçao de coookies
WebDriverWait(browser, 1).until(
    EC.presence_of_element_located((By.XPATH, '//button[@id=\
                                "onetrust-accept-btn-handler"]'))
)
print('Botão Cokkies encontrado...Ok')

# Clicando no botão correspondente a aceitar os cokkies d navegação
browser.switch_to.default_content()
button_cokkies = browser.find_element(By.XPATH, '//button[@id=\
                                "onetrust-accept-btn-handler"]')
button_cokkies.click()

print('Botão Cokkies fechado...Ok')
sleep(1)


# # Definindo a Função que extrai os dados de cada tabela
# def return_rows(list_data: list):
#     elemento = browser.find_elements(By.XPATH, "//tbody \
#             [@class='stats-table__container statsTableContainer']")
#     for elementos in elemento:
#         FIND = elementos.text.split('\n')
#         list_data.append(FIND)
#     return list_data


# # Definindo a Função que salva os dados no excel
# def save_to_excel(list: list):
#     planilha = []
#     partes = []

#     for lista_interna in list:
#         # Dividir a lista interna em partes de 5 elementos
#         partes = [lista_interna[i:i+3]for i in range(0, len(lista_interna), 3)]

#     # Adicionar cada parte como uma linha na planilha
#     planilha.extend(partes)

#     df = pd.DataFrame(planilha)
#     df.to_excel(f'clubs_{url}_new.xlsx', index=False)

#     return None


# Criando um loop para iterar sobre as variaveis de URLS
for index, url in enumerate(VARS_URLS):

    # Acessando a nova página
    print('Acessando a nova página URL.....Ok')
    browser.switch_to.new_window(url)
    browser.get(URL_MAIN+url)
    sleep(1)

    ''' ENCONTRANDO OS BOTÕES PARA FILTRAR A PAGINA '''

    # Encontrando o botão de filtro das temporadas
    filter_seasons = browser.find_element(
        By.XPATH, '//div[@data-dropdown-block="FOOTBALL_COMPSEASON"]')
    filter_seasons.click()
    sleep(1)
    print('Botão de Filter...Ok')

    # Selecionando o botão de todas as temporadas
    all_seasons = browser.find_element(
        By.XPATH, '//li[@data-option-name="All Seasons"]')
    all_seasons.click()
    sleep(1)
    print('Botão de All Seasons...Ok')

    # Encontrando o valor do botão que aciona a proxima pagina
    next_page_button = browser.find_element(By.XPATH, '//div[@class="paginationBtn paginationNextContainer"]')
    print('Botão de Next Page...Ok')

    # Loop While que percorre as paginas e chama a função de extração
    while True:

        try:
            print('Extraindo Dados.....')
            LISTA_DADOS = []

            elemento = browser.find_elements(By.XPATH, "//tbody \
            [@class='stats-table__container statsTableContainer']")
            for elementos in elemento:
                FIND = elementos.text.split('\n')
                LISTA_DADOS.append(FIND)

            sleep(1)
            next_page_button.click()
            sleep(1)

            if WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class=\
                                "paginationBtn paginationNextContainer"]'))
            ):
                continue

        except Exception:
            LISTA_DADOS = []
            next_page_button.click()
            print('Extraindo Dados.....')

            elemento = browser.find_elements(By.XPATH, "//tbody \
            [@class='stats-table__container statsTableContainer']")
            for elementos in elemento:
                FIND = elementos.text.split('\n')
                LISTA_DADOS.append(FIND)

            sleep(1)

            print('Exception Passed')
            break

    # invocando a função que salva os dados na planilha
    print('Salvando dados no Excel....')
    save_to_excel(LISTA_DADOS)
    sleep(1)

    # Mensagens de Finalização
    print(f'SCRAPING DE {url} FINALIZADO')
    sleep(1)
    print('Mudando de Janela....')

print('SCRAPING COMPLETO')
