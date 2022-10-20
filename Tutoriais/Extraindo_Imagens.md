![](https://i.creativecommons.org/l/by/4.0/88x31.png)

# Extraindo Imagens

O objetivo desse tutorial é ensinar o método de **extração** e **download** de imagens em sites. O script em Python não será utilizando spiders, mas simples [requisições HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Messages#:~:text=Requisi%C3%A7%C3%B5es%20HTTP%20s%C3%A3o%20mensagens%20enviadas,a%20a%C3%A7%C3%A3o%20a%20ser%20executada.). O site escolhido foi o próprio GitHub.

---
## Encontrando a imagem desejada:

- Abrir o site de escolha, clicar com o botão direito do mouse na imagem desejada e selecionar a opção "Inspecionar":<br><br>

    ![](./resources/docs/08.png)<br><br>


- Enconte a tag (img, nesse caso) correspondente à imagem marcada e os melhores parâmetros para trabalhar na extração:<br><br>

    ![](./resources/docs/09.png)<br><br>

---

## Mãos à obra! O script...

- Primeiro, caso não tenha os módulos, instale-os  (alguns já são nativos do python dependendo da sua versão):
  
~~~Shell
pip install bs4
pip install requests
pip install urllib
~~~

<br>

- Insira os módulos no seu código Python:

~~~Python
import requests
import urllib.request
from bs4 import BeautifulSoup
~~~

<br>

- Estabeleça uma conexão com o site desejado e puxe o conteúdo dele:
  
~~~Python
response = requests.get('https://github.com/') 
# Site base.

content = response.content
# Extrair o conteúdo do site.
~~~

<br>

- Em seguida, você deve fazer o [parser](https://pt.wikipedia.org/wiki/An%C3%A1lise_sint%C3%A1tica_(computa%C3%A7%C3%A3o)) da requisição HTTP para o HTML estruturado com o BeautifulSoup:
  
~~~Python
site_html = BeautifulSoup(content, 'html.parser')
# parser = analisa uma sequência que foi dada entrada para verificar sua estrutura gramatical segundo uma determinada gramática formal (REQUISICAO HTTP -> HTML ESTRUTURADO).
~~~

<br>

- Agora, é necessário encontrar aquela tag que você procurou na etapa de inspecionar:
  - Tente: 
    ~~~Python
    img = site_html.find('img', attrs={'class':'width-full height-auto js-globe-fallback-image'})

    link = img.attrs['src']
    ~~~


    1. Caso dê erro, pode ser porque algum parâmetro foi escrito errado. Nesse caso, você pode tentar usar outro atributo da tag ou verificar todas as estruturas daquele tipo:

        ~~~Python
        img = site_html.findAll('img', attrs={'class':'width-full height-auto js-globe-fallback-image'})

        print(img)
        # ou print(img.prettify())

        ~~~
        <br>

        ![](./resources/docs/10.png)<br><br>

    2. Então use:
        ~~~Python
       img = site_html.findAll('img', attrs={'class':'width-full height-auto js-globe-fallback-image'})
        # Pela estrutura do site, sabe-se que há apenas uma tag de imagem com a mesma classe, mas caso houvesse mais de uma, seria necessário identificar qual a imagem desejada.

        link = img[0].attrs['src']
        # Puxa o atributo src encontrado na primeira tag.
        ~~~
        <br><br>

- Passo final: baixar a imagem.

~~~Python
urllib.request.urlretrieve(f'{link}', 'img.png')
# Faz o download com base no link dado. O segundo parametro indica o nome do arquivo gerado.
~~~

<br>

![](./resources/docs/11.png)<br><br>

![](./resources/docs/img.png)<br><br>

---

## License
- Licensed under the [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.pt-br.html)
