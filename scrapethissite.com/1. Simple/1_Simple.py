'''
Countries of the World: A Simple Example
https://www.scrapethissite.com/pages/simple/
'''

import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.scrapethissite.com/pages/simple/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

countries = soup.find_all('div', class_='col-md-4 country')

with open('./scrapethissite.com/1. Simple/country_details.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Country', 'Capital', 'Population', 'Area'])

    for country in countries:
        country_name = country.find('h3', class_='country-name').get_text().strip()
        country_details = country.find('div', class_='country-info')

        capital = country_details.find('span', class_='country-capital').get_text()
        population = country_details.find('span', class_='country-population').get_text()
        area = country_details.find('span', class_='country-area').get_text()

        writer.writerow([country_name, capital, population, area])

print("Country details have been written to country_details.csv")