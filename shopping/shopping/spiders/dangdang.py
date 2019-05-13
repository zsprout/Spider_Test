# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from shopping.items import BookItem
from urllib.parse import quote

class DangdangSpider(Spider):
    name = 'dangdang'
    allowed_domains = ['www.dangdang.com']
    base_url = 'http://search.dangdang.com/?key='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                url = self.base_url + quote(keyword)
                yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        books = response.xpath('////*[@id="component_59"]//li')
        for book in books:
            item = BookItem()
            item['title'] = book.xpath('.//p[@class="name"]//a//@title').extract_first()
            item['image'] = book.xpath('.//a//img//@src').extract_first()
            item['price'] = book.xpath('.//p[@class="price"]//span[1]//text()').extract_first()
            item['author'] = book.xpath('.//p[@class="search_book_author"]//span[1]//a//@title').extract_first()
            item['publish'] = book.xpath('.//p[@class="search_book_author"]//span[3]//a//text()').extract_first()
            shop = book.xpath('////span[@class="new_lable1"]//text()').extract_first()
            item['store'] = shop if shop else book.xpath('.//p[@class="search_shangjia"]//a[1]//@title').extract_first()

            yield item
