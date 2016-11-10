# -*- coding: utf-8 -*-
# __author__ = "Lau"

import sys

import scrapy

from __init__ import parse_a_book
from douban.items import DoubanItem

sys.path.append('..')

reload(sys)
sys.setdefaultencoding('utf8')


class DoubanBooksSpider(scrapy.spiders.Spider):
    def __init__(self, name=None, **kwargs):
        super(DoubanBooksSpider, self).__init__(name, **kwargs)

    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = [
        'https://book.douban.com/tag/童话'
    ]

    # OVERRIDE
    def parse(self, response):
        # DEBUG
        self.log('--- A response from %s just arrived.' % response.url)

        items = []
        objs = parse_a_book(response, _xpath='div[@class="info"]/h2/a')
        # //div[@id="link-report"]//p//span[@class="all hidden"][1]//div[@class="intro"]//p intro
        for _iter_i in range(len(objs)):
            book_size = len(objs[_iter_i]['title'][0])
            for _iter_j in range(book_size):
                item = DoubanItem
                item['title'] = objs[_iter_i]['title'][0][_iter_j]
                item['_id'] = objs[_iter_i]['_id'][0][_iter_j]
                items.append(item)
                yield item
        print len(items)
