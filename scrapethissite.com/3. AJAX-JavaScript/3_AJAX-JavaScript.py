'''
Oscar Winning Films: AJAX and Javascript
https://www.scrapethissite.com/pages/ajax-javascript/
'''
import json
from dataclasses import dataclass

import httpx
import pandas as pd


@dataclass
class Movies:
  title: str
  year: int
  awards: int
  nominations: int
  best_picture: bool


base_url = "https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year="
year = 2010
movie_collection = []

while True:
  url = base_url + str(year)
  response = httpx.get(url)
  json_data = response.text
  movies = json.loads(json_data)
  # Define the names of the variables
  fields = ['title', 'year', 'awards', 'nominations', 'best_picture']
  # Define where the csv should be saved
  filename = "./scrapethissite.com/3. AJAX-JavaScript/movies.csv"

  for movie in movies:
    title = movie['title'].strip()
    year = movie['year']
    awards = movie['awards']
    nominations = movie['nominations']
    best_picture = bool(movie.get('best_picture', False))
    movie_collection.append(
        Movies(title, year, awards, nominations, best_picture))

  # Ensure we leave the loop if the year yields no more movies
  if len(movies) == 0:
    break
  year += 1

df = pd.DataFrame(movie_collection)
df.to_csv("./scrapethissite.com/3. AJAX-JavaScript/movies.csv", index = False)