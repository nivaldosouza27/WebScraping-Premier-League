import requests
import re
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

# Configurando as conexões
url = ('https://www.premierleague.com/stats/top/players/goals')
header = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/118.0.0.0 Safari/537.36"}

page = requests.get(url, headers=header)

soup = BeautifulSoup(page.content, 'html.parser')


# Extraindo o valor do ranking
l_rank = soup.find_all("td", {'class': 'stats-table__rank'})

# Extraindo o nome dos jogadores
l_player = soup.find_all("a", {'class': 'playerName'})

# Extraindo as logos
l_logos = soup.find_all(
    "img", {'class': 'badge-image badge-image--25 js-badge-image'}
)

# Extraindo o nome dos clube
l_club_name = soup.find_all(
    "a", {'class': 'stats-table__cell-icon-align'}
)

# Extraindo a nacionalidade do jogador
l_nacionality = soup.find_all(
    "span", {'class': 'stats__player-country'}
)

# Extraindo a estatistica filtrada
stats = soup.find_all(
    "td", {'class': 'stats-table__main-stat'}
)

# Criando uma lista de irá receber os dados
lista_dados_PL = []

# Iterando sobre os dados para retornar dentro da lista
for (ranking, players, logo, club, country, stat) in zip(l_rank, l_player, l_logos, l_club_name, l_nacionality, stats):

    ranking_player = ranking.get_text().replace(".", "")

    players_name = players.get_text()

    url_logo = logo['src']

    name_club = club.get_text()
    name_club = re.sub(r"[\n\t\s]*", "", name_club).replace('\n', '')

    nacionality = country.text

    stat_filter = stat.text

    # print(f'{ranking_player} - {players_name} - {url_logo} - {name_club} - {nacionality} - {stat_filter} ')

    lista_dados_PL.append((ranking_player, players_name,
                          name_club, nacionality, stat_filter))

for dados in lista_dados_PL:
    # print(dados)

    df_dados_PL = pd.DataFrame(dados)
    print(df_dados_PL)
