import requests
from bs4 import BeautifulSoup as soup
url = 'https://www.tripadvisor.in/AttractionProductReview-g297701-d15142407-Ubud_Tour_Best_of_Ubud_All_Inclusive-Ubud_Gianyar_Regency_Bali.html'

response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})

# bsobj = soup(html.content,'lxml')
# print(bsobj)

bsobj = soup(response.text, 'lxml')

# hotel = []
for name in bsobj.findAll('div',{'class':'biGQs _P fiohW hzzSG uuBRH'}):
    print(name.text)
#   hotel.append(name.text.strip())

# print(response.text)