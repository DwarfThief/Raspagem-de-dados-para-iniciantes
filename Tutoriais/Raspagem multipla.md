![](https://i.creativecommons.org/l/by/4.0/88x31.png)
# Raspagem múltipla
Para essa etapa, vamos acessar um site do mesmo domínio [quotes](http://quotes.toscrape.com/), ao acessar o site você verá que existe mais cards, sendo assim, mais coisa para minerar. Mãos a obra!
![](https://i.gifer.com/259T.gif)
Primeiro, vamos abrir o shell:
```
scrapy shell http://quotes.toscrape.com/
```
## Hora de testar os antigos códigos
Vamos testar os códigos básico e vê se conseguimos tirar algo com eles... Vamos tentar com os autores do texto.
```
response.css('small.author::text').extract_first()
```
Mas lembre que eu usei o `extract_first()` porque eu queria a primeira variável do Array, vamos ver o que acontece se eu pegar todo o array agora.
```
response.css('small.author::text').extract()
```
Exatamente o que queriamos, um Array de String com todos os autores. Agora vamos testar com os textos...
```
response.css('span.text::text').extract()
```
Também Funciona! Vamos testar com as tags.
```
response.css('a.tag::text').extract()
```
## Precisamos mudar de estratégia
Com certeza não vamos ser capazes de saber qual a qual texto a tag se refere, com certeza isso não vai funcionar pra gente. Vamos ter que mudar a maneira de como extraimos os dados, vamos voltar a inspecionar o código fonte do site. Perceba que os quotes (caixas onde possuem os textos) estão dentro de `<div class = 'quote'>`, então vamos extrair o `<div>` inteiro e ver no que resulta.
```
response.css('div.quote')
```
Vai sair isso:
```HTML
[<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype="h'>,
 <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype="h'>,
 <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype="h'>,
 <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype="h'>,
 <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype="h'>,
 <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype="h'>,
 <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype="h'>,
 <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype="h'>,
 <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype="h'>,
 <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype="h'>]
```
Então vamos receber mais uma vez, um Array de Strings, vamos pegar apenas uma dessas Strings e analisar.
```
quote = response.css(div.quote)[0]
```
e como saída teremos:
```HTML
<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype="h'>
```
Vamos acessar os dados desse Quote, é só trocar tudo o que for response pelo nome da variável, que no nosso caso é quote. Vejamos:
```
quote.css('small.author::text').extract_first()
quote.css('span.text::text').extract_first()
quote.css('a.tag::text').extract()
```
Beleza, tudo funcionando como queriamos, proximo passo, fazer o mesmo com os outros quotes, para isso vamos fazer um loop.
```Python
for quote in response.css('div.quote'):
    caixa = {
        'autor': quote.css('small.author::text').extract_first(),
        'texto': quote.css('span.text::text').extract_first(),
        'categorias': quote.css('a.tag::text').extract(),
    }
    print(caixa)
```
## Nosso código final vai estar assim:
Vamos editar nossa antiga Spider, lembrando de mudar sua url para a url atual e adicionar o loop dentro da Spider, ficando assim:
```Py
# -*- coding: utf-8 -*-
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/random']

    def parse(self, response):
        for quote in response.css('div.quote'):
            caixa = {
                'autor': quote.css('small.author::text').extract_first(),
                'texto': quote.css('span.text::text').extract_first(),
                'categorias': quote.css('a.tag::text').extract(),
            }
            yield caixa
```