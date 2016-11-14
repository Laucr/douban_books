# -*- coding: utf-8 -*-
# __author__ = "Lau"


def parse_a_book(response, _xpath):
    sel = response.xpath(_xpath)
    _l = []
    for a_sel in sel:
        pair = {'title': a_sel.xpath('/text()').extract(),
                '_id': a_sel.xpath('/@href').extract()}
        print a_sel.xpath('/@href').extract()
        _l.append(pair)

    return _l
