![](https://i.creativecommons.org/l/by/4.0/88x31.png)
# Primeira Spider
Primeiro, vamos criar nossa Spider usando o comando scrapy genspider quotes toscrape.com, o parâmetro quotesé o nome da nossa aranha, normalmente nomeamos elas pelo nome do site, ja o segundo parâmetro é o domínio que ela visitará.
```
scrapy genspider quotes toscrape.com
```
## Entendendo a Spider:
Criado a nossa spider, vamos editar o quotes.py. O código vai estar assim:
```Python
# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://toscrape.com/']

    def parse(self, response):
        pass
```
Como podemos ver, a aranha é do tipo classe classe e ela possui alguns atributos, vejamos...
* name: É o nome que foi dado durante sua criação e é o nome que usaremos para ativa-lá.
* allowed_domains: São os dominios que a aranha pode ir, usamos isso para certificar que a aranha não irá para domínios que não são permitidos (acessar um domínio errado pode gerar problemas com a lei, cuidado).
* start_urls: É o url inical quando a aranha for executada.
## Editando a Spider:
Vamos começar a editar nossa Spider, ela não veio perfeita... **Mãos a obra!**
1. Mudando o **start_urls**:
    * Essa é rápida, devemos alterar o url inicial, visto que este não é o url que queremos, ele deve ficar assim:
    `start_urls = ['http://quotes.toscrape.com/random']`
2. Editando o `def parse(self, response)`:
    * Essa parte é importante, esse método é chamado toda vez que a aranha é executada, sendo assim, o que estiver dentro deste método será executado no seu início. Vamos testar isso fazendo com que nossa aranha nos mande uma mensagem durante sua invocação.
    ```Python
    def parse(self, response):
        self.log(\"Eu estou viva e caminhei pelo \"+ response.url)
    ```
    * Agora rode sua aranha usando o comando no seu terminal:
    ```
    scrapy runspider quotes.py
    ```
    * Você vai perceber que vários textos serão impressos, no momento, abstraia e procure pela sua mensagem, ela deve estar por ai... Agora vamos dificultar as coisas, primeiro vamos criar um generator para a informação e declarar as informações que queremos guardar, dessa forma:
    ```Python
    def parse(self, response):
        yield{
            'text':response.css('span.text::text').extract_first() ,
            'autor':response.css('small.author::text').extract_first() ,
            'categorias':response.css('a.tag::text').extract() , 
        }
    ```
    * Agora vamos rodar a spider novamente:
    ```
    scrapy runspider quotes.py
    ```
    * Você vai notar que a Spider extraiu a informação do site, procure no meio da bagunça! Agora vamos salvar essa informação em um .json, é bem simples:
    ```
    scrapy runspider quotes.py -o site.json
    ```
    * Agora vamos ver o que a nossa aranha salvou no arquivo, para isso vamos rodar o comando:
    ```
    more site.json
    ```
## Então o código final deve estar assim:
```Python
# -*- coding: utf-8 -*-
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/random']

    def parse(self, response):
        yield{
            'text':response.css('span.text::text').extract_first() ,
            'autor':response.css('small.author::text').extract_first() ,
            'categorias':response.css('a.tag::text').extract() , 
        }
```