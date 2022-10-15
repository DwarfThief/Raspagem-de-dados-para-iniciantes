import requests
import urllib.request
from bs4 import BeautifulSoup

# Estabelecendo conexão com o servidor da página e puxando o conteúdo.
response = requests.get('https://www.nytimes.com/international/')
content = response.content
site_html = BeautifulSoup(content, 'html.parser')

# Encontrando o elemento desejado.
img = site_html.findAll('img', attrs={'alt':'Visitors to the ONX Studio in Manhattan with Ashley Zelinskie’s “Ring Nebula” (2022), a 3-D printed sculpture, during the exhibition “Unfolding the Universe.”'})
link = img[1].attrs['src']

# Realizando o download a partir do img src.
urllib.request.urlretrieve(f'{link}', 'img.png')
