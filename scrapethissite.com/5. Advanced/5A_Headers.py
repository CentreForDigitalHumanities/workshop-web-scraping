'''
Spoofing Headers
https://www.scrapethissite.com/pages/advanced/?gotcha=login
'''
# Solution:
# Network > click on request > see 'Headers' in right panel 
# We only care about Request Headers 
# Save the headers as a dictionary 
# Give it to the 'headers' argument in the response call. 
# --> Maybe this can be extracted automatically? 

import httpx
from bs4 import BeautifulSoup

# Not sure if this only works for my machine?! 
headers = {
    "Accept": "text/html,*/*;q=0.9",
    #"Accept-Encoding": "gzip, deflate, br, zstd", had to remove this one to ensure 
    # readable output
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Content-Length": "0",
    "Content-Type": "text/html; charset=utf-8",
    "Origin": "https://www.scrapethissite.com",
    "Priority": "u=1, i",
    "Referer": "https://www.scrapethissite.com/",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

url = "https://www.scrapethissite.com/pages/advanced/?gotcha=headers"
response = httpx.get(url, headers = headers)

# Extra to print the text
soup = BeautifulSoup(response.content, 'html.parser')
text = soup.find('div', class_= 'col-md-4 col-md-offset-4').text.strip()
print(text)
