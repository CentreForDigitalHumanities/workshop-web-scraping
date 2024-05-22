'''
Hockey Teams: Forms, Searching and Pagination
https://www.scrapethissite.com/pages/forms/
'''

from dataclasses import dataclass
import httpx
import pandas as pd
from bs4 import BeautifulSoup


@dataclass
class HockeyTeam:
  name: str
  year: int
  pct: float


base_url = "https://www.scrapethissite.com/pages/forms/?page_num="
hockeyteams = []
page_nr = 1
while True:
  url = base_url + str(page_nr)
  response = httpx.get(url)
  html = response.text
  soup = BeautifulSoup(html, "html.parser")
  teams = soup.find_all("tr", class_="team")

  if len(teams) == 0:  # Ensure scraping stops when we run out of teams
    break

  for team in teams:
    name = team.find("td", class_="name").text.strip()
    year = team.find("td", class_="year").text.strip()
    pct = team.find("td", class_="pct").text.strip()
    hockeyteam = HockeyTeam(name=name, year=year, pct=pct)
    hockeyteams.append(hockeyteam)
  page_nr += 1
#breakpoint()

df = pd.DataFrame(hockeyteams)

df.to_csv("./scrapethissite.com/2. Forms/hockeyteams.csv", index = False)
