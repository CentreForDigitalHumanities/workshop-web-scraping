'''
Logins & Session Data
https://www.scrapethissite.com/pages/advanced/?gotcha=login
'''

# Sources I tried: 
# https://blog.hartleybrody.com/web-scraping-cheat-sheet/#sessions-and-cookies


import requests

session = requests.Session()
print(session.cookies.get_dict())

response = session.get("https://www.scrapethissite.com/pages/advanced/?gotcha=login")
print(session.cookies.get_dict())

response = session.get("https://uu.nl")
print(session.cookies.get_dict())

response = session.get("https://google.com")
print(session.cookies.get_dict())

# Ik snap niet waarom het wel werkt voor Google maar niet voor de andere sites 


