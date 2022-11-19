import requests
from bs4 import BeautifulSoup as soup
url = 'https://www.tripadvisor.in/Hotels-g187147-Paris_Ile_de_France-Hotels.html'

response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})

# bsobj = soup(html.content,'lxml')
# print(bsobj)

bsobj = soup(response.text, 'lxml')

hotel = []
for name in bsobj.findAll('div',{'class':'listing_title'}):
  hotel.append(name.text.strip())

print(hotel)