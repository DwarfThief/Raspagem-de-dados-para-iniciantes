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