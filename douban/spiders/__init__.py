# -*- coding: utf-8 -*-
# __author__ = "Lau"


def parse_a_book(response, _xpath):
    sel = response.xpath('//' + _xpath)
    _l = {'title': [],
          '_id': []}
    for a_sel in sel:
        title = a_sel.xpath('.//' + '/text()').extract()
        _id = a_sel.xpath('.//' + '/@href').extract().split('/')[-1]
        _l['title'].append(title)
        _l['_id'].append(_id)
        return _l
