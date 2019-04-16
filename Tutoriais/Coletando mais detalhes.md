![](https://i.creativecommons.org/l/by/4.0/88x31.png)
# Coletando mais detalhes
Nós ja coletamos frases, o autor e suas categorias. Mas isso não é tudo que nossa Spider pode fazer, mas ainda tem coisa que nós não pegamos do site. Vamos voltar para o [site](http://quotes.toscrape.com/), note que do lado de cada autor tem o `(about)`, esse botão nos leva para uma parte do site onde fala sobre o autor. Então vamos coletar isso também.
![](https://media.giphy.com/media/l1IY0geomfz09dEB2/giphy.gif)
## Hora de inspecionar!
Ao inspecionar o botão vamos ver que ele fica dentro de um `<a>` que fica dentro de um `<span>` que fica dentro de um `<div class=\"quote\">` e que no final de tudo, ele da um `href` pra gente... Rolou um Déjà vu? Sim, nos ja vimos isso quando aprendemos sobre [Navegação entre páginas](https://github.com/DwarfThief/Raspagem-de-dados-para-iniciantes/blob/master/Navegando%20entre%20paginas.ipynb), então vamos fazer o mesmo.

**1. Vamos criar uma só para extrair esses detalhes. É só fazer `scrapy genspider autores toscrape.com/`.**

**2. Agora vamos extrair os links dentro do href (coloque isso dentro do método `parse`):**

```
autores_urls = response.css('div.quote > span > a::attr(href)').extract()
```

Como resposta, recebemos uma List de Strings, essas Strings são sobre todos os autores que estão na página.

**3. Agora vamos criar um loop para varrer essa Lista e acessar o site (também dentro do `parse`).**

```Python
for url in autores_urls:
    url = response.urljoin(url)
    yield scrapy.Request(url=url, callback=self.parse_detalhes)
```
O código ta bem parecido com o que fizemos no [Notebook anterior](https://github.com/DwarfThief/Raspagem-de-dados-para-iniciantes/blob/master/Navegando%20entre%20paginas.md), mas note que no parâmetro de `callback=` eu não coloquei o `self.parse`, em vez disso eu coloquei `self.parse_detalhes`. Sendo assim ele irá para a função `parse_detalhes`, vai ser nessa função que vamos colher os dados.

**4. Hora de criar a função `parse_detalhes`.**

```Python
def parse_detalhes(self, response):
```

Beleza, agora nos temos nossa função, mas ela ta vazia. Lembrando que essa função foi feita para colher os dados. **Vamos inspecionar**, mas dessa vez temos que inspecionar a página do autor, abra qualquer uma. Temos três informações ai, o nome, a data de aniversário e a biografia.

* Inspecionando o nome:
    Vamos descobrir esse caminho `response.css('h3.author-title::text')`, lembrando que devemos extrair a String, sendo assim, `response.css('h3.author-title::text').extract_first()`.
* Inspecionando a data de aniversário:
    Vamos descobrir esse caminho `response.css('span.author-born-date::text').extract_first()`.
* inspecionando a biografia: 
    Vamos descobrir esse caminho `response.css('div.author-description::text').extract_first()`.

Perfeito! Agora vamos colocar isso dentro de um `yield`, eu fiz dessa maneira:
```Python
def parse_detalhes(self, response):
    yield {
        'nome' : response.css('h3.author-title::text').extract_first(),
        'aniversario' : response.css('span.author-born-date::text').extract_first(),
        'detalhes' : response.css('div.author-description::text').extract_first(),
    }
```
## Nosso código final vai estar assim:
```Python
# -*- coding: utf-8 -*-
import scrapy


class AutoresSpider(scrapy.Spider):
    name = 'autores'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        #Colhendo os detalhes dos autores       
        autores_urls = response.css('div.quote > span > a::attr(href)').extract()
        for url in autores_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_detalhes)

        #Navegação entre páginas
        proxima_pag = response.urljoin(response.css('li.next > a::attr(href)').extract_first())
        yield scrapy.Request( url = proxima_pag, callback = self.parse)

    def parse_detalhes(self, response):
        yield {
            'nome' : response.css('h3.author-title::text').extract_first(),
            'aniversario' : response.css('span.author-born-date::text').extract_first(),
            'detalhes' : response.css('div.author-description::text').extract_first(),
        }
```
* Para executar:
```
scrapy runspider autores.py
```
* Caso queira colocar os dados em um arquivo, escreva:
```
scrapy runspider autores.py -o autores.json
```