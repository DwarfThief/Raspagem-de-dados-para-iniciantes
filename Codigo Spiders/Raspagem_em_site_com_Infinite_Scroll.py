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