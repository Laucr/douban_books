# -*- coding: utf-8 -*-
# __author__ = "Lau"

import sys

import scrapy

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
    def start_requests(self):
        yield scrapy.Request("https://book.douban.com/tag/童话",
                             headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) "
                                                    "\Gecko/20100101 Firefox/48.0"})

    # OVERRIDE
    def parse(self, response):
        # DEBUG
        self.log('--- A response from %s just arrived.' % response.url)

        items = []
        # objs = parse_a_book(response, _xpath='//div[@class="info"]/h2/a')

        item_size = len(response.xpath('//div[@class="info"]/h2/a'))
        # I love this line :>
        _l = [{'title': [a_title.extract() for a_title in response.xpath('//div[@class="info"]/h2/a/@title')][_iter],
               '_id': [a_id.extract().split('/')[-2] for a_id in response.xpath('//div[@class="info"]/h2/a/@href')]
               [_iter]} for _iter in range(item_size)]

        print _l

        # //div[@id="link-report"]//p//span[@class="all hidden"][1]//div[@class="intro"]//p intro
        # for _iter_i in range(len(objs)):
        #     book_size = len(objs[_iter_i]['title'][0])
        #     for _iter_j in range(book_size):
        #         item = DoubanItem
        #         item['title'] = objs[_iter_i]['title'][0][_iter_j]
        #         item['_id'] = objs[_iter_i]['_id'][0][_iter_j]
        #         items.append(item)
        #         yield item
        print len(items)
