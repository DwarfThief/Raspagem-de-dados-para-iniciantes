![](https://i.creativecommons.org/l/by/4.0/88x31.png)

# Aprendendo a extrair texto de um site com Scrapy
Nosso código vai acessar o site [toscrape](http://quotes.toscrape.com/random), esse código irá retirar as frases, o nome do Autor e a categoria que o texto se enquadra. Para isso, devemos iniciar o Shell do Scrapy.
No seu terminal, rode:
```
scrapy shell http://quotes.toscrape.com/random
```
Agora devemos analisar o código base do site, ao apertar F12, o painel de desenvolvedor é aberto. Colocando o mouse sobre a frase, clique com o botão direito do mouse ou Ctrl + Shift + I para inspecionar a frase. Uma linha do código fonte da página sera destacado, algo como:

```HTML
<span class="text" itemprop="text">[FRASE]</span>
```

Sabendo onde se encontra o texto, devemos extraí-lo, para isso usamos o método response.css(), para localizar o texto no arquivo .css, depois esclarecemos a tag e o nome da classe, o que resultaria span.text. No final o codigo ficaria:
```
response.css('span.text')
```
Mas você vê que o texto não sai limpo, sai algo como `[<Selector xpath="descendant-or-self::span[@class and contains(concat(' ', normalize-space(@class), ' '), ' text ')]/text()" data=" [TEXTO] ">]`. Precisamos tratar isso, então usaremos o método .extract(), o código agora ficara algo como:
```
response.css('span.text')
```
Retornou um array com o texto dentro, mas o array só possui uma String, então vamos acessar esse array.
```
response.css('span.text').extract_first()
```
## Agora vamos extrair o autor da frase.

Vamos extrair as categorias da frase, mesmo passo-a-passo.

1. Inspecionar o elemento e descobrir sua localização no código fonte da página.
2. Esclarecer a tag e classe para extrairmos o texto.

```
response.css('a.tag::text').extract()
```
Mas dessa vez queremos todo o Array, visto que uma frase pode ter mais de uma categoria ligada a ela.