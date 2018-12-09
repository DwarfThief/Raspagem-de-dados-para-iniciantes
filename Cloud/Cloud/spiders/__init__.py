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