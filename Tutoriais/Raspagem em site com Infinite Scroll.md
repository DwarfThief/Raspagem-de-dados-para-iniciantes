![](https://i.creativecommons.org/l/by/4.0/88x31.png)
# Raspagem em site com Infinite Scroll
Agora vamos aprender como lidar com sites que utilizam **infinite scroll**. Infinite Scroll é uma técnica usada em muitos sites para ficar carregando sempre informação na tela do usuário, assim não vai existir um botão na tela chamado `next` para passar as páginas, pois não existirão páginas.

O nosso site de teste será [uma versão do quotes](http://quotes.toscrape.com/scroll). Sempre que rolarmos para baixo, o site carrega mais informação pra gente, mas como isso acontece?

## Hora de inspecionar!

Dessa vez não iremos olhar o código, ainda, vamos olhar a tabela chamada *\"networking\"*. Coloque nessa tabela e desça a página até as informações serem atualizadas. Ao descer a página o browser faz um novo request para o servidor, que retorna um arquivo .json onde contém os arquivos. Sendo assim, a informação ja está estruturada para a gente, nós apenas precisamos salva-lá em um arquivo. Então vamos fazer o request com a nossa Spider e extrair o arquivo.

Dentro da tabela **`Network`** existe uma tabela chamada **`headers`**, dentro dela vai existir um link url de onde veio nosso arquivo .json, vamos usar isso na nossa Spider.

## Hora de codar

* Vamos ver o que vem dentro desse url que pegamos. Para isso vamos abrir o shell do scrapy:
```
scrapy shell http://quotes.toscrape.com/api/quotes?page=1
```
* Agora vamos criar nossa spider, digite no terminal:
```
scrapy genspider infinite_scroll quotes.com
```
Seu código vai estar assim:
```Py
# -*- coding: utf-8 -*-
import scrapy

class InfiniteScrollSpider(scrapy.Spider):
    name = 'infinite_scroll'
    allowed_domains = ['quotes.com']
    start_urls = ['http://quotes.com/']

    def parse(self, response):
        pass
```
* No `start_urls` vamos colocar o link q pegamos no headers:
```
start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']
```
Agora vamos ver o que conseguimos extrair desse site, no shell do Scrapy, rode:
```
response.text
```
* Aqui esta nosso .json, guardar essas informações em uma variável, assim:
```
dados = json.loads(response.text)
```
* Agora devemos dividir isso em um dicionário para salva. Olhando o arquivo .json percebemos que ele esta dividido em author_name, text e tags. Vamos criar um yield para guardar essas informações. Isso tudo dentro de um for, assim ele irá percorrer todas as frases da página e repetir o processo.
```Py
for frase in dados['quotes']:
    yield {
        'name_author': frase['author']['name'],
        'texto': frase['text'],
        'categorias': frase['tags'],
    }
```
**Traduzi as divições, mas possuem a mesma funcionalidade.**

* Agora ele acessa os Quotes, extraindo as informações de acordo com suas categorias e salvando no nosso dicionário, mas agora precisamos acessar as demais páginas.

* Ainda dentro da função parse, usando o has_next nos dados vamos checar se existe na página antes de prosserguimos. É só colocar isso dentro de um if, vai ficar assim:
```Py
if dados['has_next']:
```
* Agora vamos prosseguir para as próximas páginas.
```Py
if dados['has_next']:
    proxima_pag = dados['page'] + 1
    yield scrapy.Request(url=self.api_url.format(proxima_pag), callback=self.parse)
```
* Pronto, agora nosso código é capaz de extrair todas as informações dessa API e guardar no seu próprio dicionário.
## Então o código final deve estar assim:
```Py
# -*- coding: utf-8 -*-
import scrapy
import json

class InfiniteScrollSpider(scrapy.Spider):
    name = 'infinite_scroll'
    allowed_domains = ['quote.com']
    start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        dados = json.loads(response.text)
        for frase in dados['quotes']:
            yield {
                'name_author': frase['author']['name'],
                'texto': frase['text'],
                'categorias': frase['tags'],
            }

        if dados['has_next']:
            proxima_pag = dados['page'] + 1
            yield scrapy.Request(url=self.api_url.format(proxima_pag), callback=self.parse)
```