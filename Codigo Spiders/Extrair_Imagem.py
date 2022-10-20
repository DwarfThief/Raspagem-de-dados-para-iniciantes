import requests
import urllib.request
from bs4 import BeautifulSoup

# Estabelecendo conexão com o servidor da página e puxando o conteúdo.
response = requests.get('https://github.com/')
content = response.content
site_html = BeautifulSoup(content, 'html.parser')

# Encontrando o elemento desejado.
img = site_html.find('img', attrs={'class':'width-full height-auto js-globe-fallback-image'})
link = img.attrs['src']

# Realizando o download a partir do img src.
urllib.request.urlretrieve(f'{link}', 'img.png')
