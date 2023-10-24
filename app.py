from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from bs4 import BeautifulSoup
import openpyxl


ROOT_FOLDER = Path(__file__).parent
ROOT_FILE = ROOT_FOLDER / 'chromedriver.exe'
ROOT_CHROME_DRIVER = str(ROOT_FILE)
CONTENT = ''


# Configurando as conexões de serviço
service = Service(executable_path=ROOT_CHROME_DRIVER)

# Configurando as options do webdriver
options = Options()
options.add_argument('window-size=1080,1920')
# options.add_argument('--headless')

# Configurando o browser e URL de Acesso
browser = webdriver.Chrome(service=service, options=options)
browser.get('https://www.premierleague.com/stats/top/players/goals')

# Tempo de Espera para carregar os elementos da pagina
sleep(2)

# Encontrando o botão de filtro das temporadas
filter_seasons = browser.find_element(
    By.XPATH, '//div[@data-dropdown-block="FOOTBALL_COMPSEASON"]')
filter_seasons.click()
sleep(1)

# Selecionando o botão de todas as temporadas
all_seasons = browser.find_element(
    By.XPATH, '//li[@data-option-name="All Seasons"]')
all_seasons.click()

sleep(1)

# Usando Beautiful Soup para identificar a pagina
soup = BeautifulSoup(browser.page_source, 'html.parser')

# Declarando a lista principal de dados
list_data = []
lista_completa = []

# Encontrando o valor do botão proxima pagins
next_page_button = browser.find_element(
    By.XPATH, '//div[@class="paginationBtn paginationNextContainer"]')

# Função que extrai os dados


def return_rows(list_data: list, lista_completa: list):
    table_rows = soup.find_all("tr", {'class': 'table__row'})
    for i in range(10):
        CONTENT = table_rows[i].contents
        for i, valor in enumerate(CONTENT):
            Content_Line = CONTENT[i].text
            Unique_Values = [' ', '\xa0']
            if Content_Line not in Unique_Values:
                list_data.append(Content_Line.strip())
            lista_completa.extend(list_data)
            list_data = []

    return print(lista_completa)


while next_page_button == browser.find_element(By.XPATH, '//div[@class="paginationBtn paginationNextContainer"]'):

    next_page_button.click()

    wait = WebDriverWait(browser, 2)
    element = wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "paginationBtn paginationNextContainer")))

    return_rows(list_data, lista_completa)

    sleep(2)

# for i in range(10):
#     content = table_rows[i].contents

#     for i, valor in enumerate(content):
#         Content_Line = content[i].text
#         Unique_Values = [' ', '\xa0']
#         if Content_Line not in Unique_Values:
#             list_data.append(Content_Line.strip())


# # Iniciando o loop para clicar no botão proxima pagina e carregar os dados.
# while next_page_button == browser.find_element(By.XPATH, '//div[@class="paginationBtn paginationNextContainer"]'):

#     try:
#         # Função que retorna os dados de cada linha
#         def return_rows(posicao: int, lista_dados: list):

#             table_rows = soup.find_all("tr", {'class': 'table__row'})
#             content = table_rows[posicao].contents

#             for i, valor in enumerate(content):
#                 Content_Line = content[i].text
#                 Unique_Values = [' ', '\xa0']
#                 if Content_Line not in Unique_Values:
#                     lista_dados.append(Content_Line.strip())
#             return lista_dados

#         # Função que salve os dados em uma lista

#         def exec_func_rows(func, list: list):
#             for i in range(10):
#                 func(i, list)

#             # # Gurdando todos os dados no Excel
#             workbook = openpyxl.load_workbook('dados.xlsx')
#             sheet = workbook['Dados']

#             # Calcule em qual linha começar a adicionar os dados
#             # Comece a partir da linha 2 (a primeira linha é para cabeçalhos)
#             linha_inicio = 2

#             # Use um loop para inserir os dados na planilha
#             for i, item in enumerate(list, start=1):
#                 coluna = (i - 1) % 5 + 1  # Calcula a coluna (1, 2, 3, 4 ou 5)
#                 sheet.cell(row=linha_inicio, column=coluna, value=item)
#                 if i % 5 == 0:
#                     linha_inicio += 1  # Mude para a próxima linha a cada 5 itens

#             # Salve o arquivo Excel
#             workbook.save('dados.xlsx')

#         # Chamando a função principal
#         exec_func_rows(return_rows, list_data)

#         sleep(1)

#         next_page_button.click()

#     except Exception:
#         break
#     continue
