# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class BookItem(Item):
    collection = "books"
    title = Field()
    image = Field()
    price = Field()
    author = Field()
    publish = Field()
    store = Field()

