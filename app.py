import requests
import re
from bs4 import BeautifulSoup

# Configurando as conexões
url = 'https://www.premierleague.com/stats/top/players/goals'
header = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/118.0.0.0 Safari/537.36"}

page = requests.get(url, headers=header)
soup = BeautifulSoup(page.content, 'html.parser')


# Extraindo o valor do ranking
rank = soup.find_all("td", {'class': 'stats-table__rank'})
for ranking in rank:
    ranking_player = ranking.get_text().replace(".", "")

# Extraindo o nome dos jogadores
player = soup.find_all("a", {'class': 'playerName'})
for players in player:
    players_name = players.get_text()

# Extraindo o nome dos clube
tags_url = soup.find_all(
    "a", {'class': 'stats-table__cell-icon-align'}
)
for tag in tags_url:
    name_club = tag.get_text()
    name_club = re.sub(r"[\n\t]", "", name_club).replace(' ', '', 10)

logos = tags_url.find_all(
    "img", {'class': 'badge-image badge-image--25 js-badge-image'}
)
print(logos)
