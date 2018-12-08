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