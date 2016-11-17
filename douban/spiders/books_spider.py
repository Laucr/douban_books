# -*- coding: utf-8 -*-
# __author__ = "Lau"

import sys
import urllib

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
        'https://book.douban.com/tag/%E5%84%BF%E7%AB%A5%E6%96%87%E5%AD%A6',  # 儿童文学
        # 'https://book.douban.com/tag/%E5%8E%86%E5%8F%B2',  # 历史
        # 'https://book.douban.com/tag/%E6%8E%A8%E7%90%86',  # 推理
        # 'https://book.douban.com/tag/%E7%BE%8E%E9%A3%9F',  # 美食
        # 'https://book.douban.com/tag/%E6%97%85%E8%A1%8C',  # 旅行
        # 'https://book.douban.com/tag/%E7%BB%8F%E6%B5%8E%E5%AD%A6',  # 经济学
        # 'https://book.douban.com/tag/%E4%BA%92%E8%81%94%E7%BD%91',  # 互联网
        # 'https://book.douban.com/tag/%E9%9F%B3%E4%B9%90',  # 音乐
        # 'https://book.douban.com/tag/%E6%95%B0%E5%AD%A6',  # 数学
        # 'https://book.douban.com/tag/%E7%A4%BE%E4%BC%9A%E5%AD%A6',  # 社会学
    ]

    # OVERRIDE
    def start_requests(self):
        for a_url in self.start_urls:
            # for page in range(0, 1000, 20):
            # yield scrapy.Request(url=(a_url + '?start='+ str(page) +'&type=T'),
            yield scrapy.Request(url=a_url,
                                 headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0)"
                                                        "Gecko/20100101 Firefox/48.0"})

    # OVERRIDE
    def parse(self, response):
        item_size = len(response.xpath('//div[@class="info"]/h2/a'))
        # I love this line XD
        _items = [
            {
                'title': [a_title.extract() for a_title in response.xpath('//div[@class="info"]/h2/a/@title')][_iter],
                '_id': [a_id.extract() for a_id in response.xpath('//div[@class="info"]/h2/a/@href')][_iter]
            } for _iter in range(item_size)
            ]

        for _a_item in _items:
            yield scrapy.http.Request(url=_a_item['_id'].encode('utf8'),
                                      headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0)"
                                                             "Gecko/20100101 Firefox/48.0"},
                                      meta={'title': _a_item['title'].encode('utf8'),
                                            'category': urllib.unquote(response.url.split('/')[-1])},
                                      callback=self.parse_secondary_link)

    def parse_secondary_link(self, response):
        sel = scrapy.Selector(response)
        item = {
            'title': response.meta['title'],
            'intro': sel.xpath('//*[@id="link-report"]/div[1]/div/p/text()').extract()[0].encode('utf8'),
            'category': response.meta['category']
        }
        yield item
