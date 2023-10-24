from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pathlib import Path
from bs4 import BeautifulSoup
# import openpyxl


ROOT_FOLDER = Path(__file__).parent
ROOT_FILE = ROOT_FOLDER / 'chromedriver.exe'
ROOT_CHROME_DRIVER = str(ROOT_FILE)
TABLE = None

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
filter_seasons = browser.find_element(By.XPATH, '//div[@data-dropdown-block="FOOTBALL_COMPSEASON"]')
filter_seasons.click()
sleep(1)

# Selecionando o botão de todas as temporadas
all_seasons = browser.find_element(By.XPATH, '//li[@data-option-name="All Seasons"]')
all_seasons.click()

sleep(1)

# Usando Beautiful Soup para identificar a pagina
soup = BeautifulSoup(browser.page_source, 'html.parser')


# Declarando as Listas
list1 = list2 = list3 = list4 = list5 = list6 = list7 = list8 = list9 = list10 = []

# Unindo as lista em uma lista superior
List_firts_consult = [
    [list1], [list2], [list3], [list4], [list5], [list6], [list7], [list8], [list9], [list10]
]

Lista_Completa = {}

# next_page_button = browser.find_element(By.XPATH, '//div[@class="paginationBtn paginationNextContainer"]')

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

#         # Iteravel que percorre um int para chamar a função
#         for i in range(10):
#             return_rows(i, List_firts_consult[i])

#         next_page_button.click()

#     except Exception:
#         break
#     continue


# Função que retorna os dados de cada linha
def return_rows(posicao: int, lista_dados: list, lista_completa: dict):

    table_rows = soup.find_all("tr", {'class': 'table__row'})
    content = table_rows[posicao].contents

    for i, valor in enumerate(content):
        Content_Line = content[i].text
        Unique_Values = [' ', '\xa0']
        if Content_Line not in Unique_Values:
            lista_dados.append(Content_Line.strip())
            lista_completa = {f'{i}': lista_dados}
    return lista_completa


for i in range(10):
    return_rows(i, list1, Lista_Completa)

print(Lista_Completa)



# # Gurdando todos os dados no Excel
# workbook = openpyxl.load_workbook('dados.xlsx')
# sheet = workbook['Dados']

# for i, valor in enumerate(List_firts_consult[0], start=2):
#     cell = sheet.cell(row=i, column=i)
#     cell.value = valor[0]

# workbook.save('dados.xlsx')







# # Extraindo o valor do ranking
# l_rank = soup.find_all("td", {'class': 'stats-table__rank'})

# for rank in l_rank:
#     RANK = rank.get_text().replace(".", "")
#     list_rank.append(RANK)


# # Extraindo o nome dos jogadores
# l_player = soup.find_all("a", {'class': 'playerName'})

# for player in l_player:
#     PLAYER = player.get_text().lstrip()
#     list_player.append(PLAYER)


# # Extraindo o nome dos clube
# l_hide_s = soup.find_all(
#     "td", {'class': 'hide-s'}
# )
# l_club_name = soup.find_all(
#     "a", {'class': 'stats-table__cell-icon-align'}
# )
# for club in l_club_name:
#     CLUB = club.get_text()
#     list_club.append(CLUB)


# # Extraindo a nacionalidade do jogador
# l_nacionality = soup.find_all(
#     "span", {'class': 'playerCountry'}
# )
# for country in l_nacionality:
#     COUNTRY = country.text
#     list_country.append(COUNTRY)


# # Extraindo a estatistica filtrada
# l_stats = soup.find_all(
#     "td", {'class': 'stats-table__main-stat'}
# )
# for stats in l_stats:
#     STATS = stats.text
#     list_stats.append(STATS)

# # Tempo de Carregamento dos Dados Finais
# sleep(1)

# # Gurdando todos os dados no Excel
# workbook = openpyxl.load_workbook('dados.xlsx')
# sheet = workbook['Dados']

# for i, valor in enumerate(list_rank, start=2):
#     cell = sheet.cell(row=i, column=1)
#     cell.value = valor

# for i, valor in enumerate(list_player, start=2):
#     cell = sheet.cell(row=i, column=2)
#     cell.value = valor

# for i, valor in enumerate(list_club, start=2):
#     cell = sheet.cell(row=i, column=3)
#     cell.value = valor

# for i, valor in enumerate(list_country, start=2):
#     cell = sheet.cell(row=i, column=4)
#     cell.value = valor

# for i, valor in enumerate(list_stats, start=2):
#     cell = sheet.cell(row=i, column=5)
#     cell.value = valor

# workbook.save('dados.xlsx')








# # Iterando sobre os dados para retornar dentro da lista
# for (ranking, players, club, country, stat) in zip(l_rank, l_player, club_name_result, l_nacionality, l_stats):
#     ranking_player = ranking.get_text().replace(".", "")
#     players_name = players.get_text().lstrip()
#     name_club = club
#     nacionality = country.text
#     stat_filter = stat.text

#     print(f'{ranking_player} - {players_name} - {name_club} - {nacionality} - {stat_filter}')
