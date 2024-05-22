'''
Turtles All the Way Down: Frames & iFrames
https://www.scrapethissite.com/pages/frames/
'''

from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup

import pandas as pd
import requests

@dataclass
class Turtles:
  family_name: str
  image_url: str
  lead_paragraph: str

base_url = 'https://www.scrapethissite.com/pages/frames/?frame=i&family='
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

family_names = []
information = []

for link in soup.find_all('a'):
    href = link.get('href')
    parsed = urlparse(href)
    query_params = parse_qs(parsed.query)

    if 'family' in query_params:
        family_names.append(query_params['family'][0])

for family in family_names:
  url = base_url + family
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  
  turtle_image = soup.find('img', class_='turtle-image')
  image_url = turtle_image.get('src')
  family_name = soup.find('h3', class_='family-name').get_text().strip()
  lead_paragraph = soup.find('p', class_='lead').get_text().strip()

  information.append(Turtles(family_name=family_name, image_url=image_url, 
                             lead_paragraph=lead_paragraph))
  
df = pd.DataFrame(information)
df.to_csv('./scrapethissite.com/4. Frames/turtles.csv', index=False)