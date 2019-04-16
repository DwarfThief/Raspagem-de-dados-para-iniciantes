![](https://i.creativecommons.org/l/by/4.0/88x31.png)
# Navegando entre páginas
![](https://media.tenor.com/images/f1921d017450cd690cfa73bfe33d7724/tenor.gif)

Nosso objetivo nesse Notebook será a raspagem de dados entre páginas. Nosso site continua sendo o [Quotes](http://quotes.toscrape.com/), queremos extrair a frase, o autor e a categoria de todas as frases que a página possui. No [Notebook anterior](https://github.com/DwarfThief/Raspagem-de-dados-para-iniciantes/blob/master/Raspagem%20multipla.ipynb) nos já conseguimos colher o texto de toda a página, mas... e as outras?

O nosso programa deve ser capaz de acessar o site, colher toda a informação da página, "clicar" no botão next -> e acessar a próxima página, onde ele irá repetir todo o processo. Podemos ver facilmente que isso será um loop, mas para criarmos o Loop devemos entender como o botão funciona.

## Inspecionando o botão "next"
Ao inspecionar o botão podemo sperceber que ele faz parte da categoria <li> e sua classe é next, agora vamos tentar extrair o que tem no css desse botão.

```
response.css('li.next')
```

A saída sera toda a lista de itens do objeto, mas se olhar detalhadamente para o código fonte, vamos ver que o link real está na subcategoria `<a>`, então vamos ver o que sai se extrairmos isso e a sua String junto.

```
response.css('li.next > a').extract_first()
```

Veja que esse botão ao ser clicado nos envia para a próxima página atraves do href, então oq devemos é extrair esse link. Para isso vamos extrair a referência dentro do href.

```
proxima_pag = response.css('li.next > a::attr(href)').extract_first()
```

A saída será uma String com o endereço para a próxima página, agora devemos unir essa parte com o resto do endereço que usamos no `start_urls`, então vamos usar o método `.urljoin()` e passar como parâmetro a nossa variável `proxima_pag`, assim:

```
response.urljoin(proxima_pag)
```

Agora nossa Spider extrair o endereço da próxima página, mas ainda não fizemos nada com essa informação, ta na hora de fazer com que a Spider vá para a próxima página. Precisamos guardar o novo URL em uma variável, podemos fazer, assim:

```
proxima_pag = response.css('li.next > a::attr(href)').extract_first()
proxima_pag = response.urljoin(proxima_pag)
```
ou assim:

```
proxima_pag = response.urljoin(response.css('li.next > a::attr(href)').extract_first())
```

As duas formas dão na mesma coisa, eu usarei a 2ª opção. Continuando ando com nosso programa, vamos implementar esse código dentro da nossa Spider, o código ficaria assim:

```Python
# -*- coding: utf-8 -*-
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/random']

    def parse(self, response):
        #Extraindo as citações
        for quote in response.css('div.quote'):     
            caixa = {
                'autor': quote.css('small.author::text').extract_first(),
                'texto': quote.css('span.text::text').extract_first(),
                'categorias': quote.css('a.tag::text').extract(),
            }
            yield caixa
        #Navegação entre páginas
        proxima_pag = response.urljoin(response.css('li.next > a::attr(href)').extract_first())
```

Perceba que o novo código não fica dentro do `for quote in response.css('div.quote'):`. Agora vamos usar um yield e usar o método `scrapy.Request()` do scrapy, precisamos enviar dois parâmetros, o primeiro é a url que vamos acessar, sendo assim, passamos nossa a variável `proxima_pag`. Como segundo parâmetro escrevemos `callback = self.parse`, assim ele repetirá o método parse que nos ja definimos.
```
yield scrapy.Request( url = proxima_pag, callback = self.parse)
```
## Nosso código final vai estar assim:
```Python
# -*- coding: utf-8 -*-
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        #Extraindo as citações
        for quote in response.css('div.quote'):     
            caixa = {
                'autor': quote.css('small.author::text').extract_first(),
                'texto': quote.css('span.text::text').extract_first(),
                'categorias': quote.css('a.tag::text').extract(),
            }
            yield caixa
        #Navegação entre páginas
        proxima_pag = response.urljoin(response.css('li.next > a::attr(href)').extract_first())
        yield scrapy.Request( url = proxima_pag, callback = self.parse)
```