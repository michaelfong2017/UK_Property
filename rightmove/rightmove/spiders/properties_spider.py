#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: michael
"""

import scrapy
from lxml.etree import iterparse
from io import BytesIO
import re

class PropertiesSpider(scrapy.Spider):
    name = 'properties'
    # allowed_domains = ["rightmove.co.uk"]
    
    '''
    https://www.rightmove.co.uk/sitemap.xml
    https://www.rightmove.co.uk/sitemap-regions-England.xml
    https://www.rightmove.co.uk/sitemap-outcodes-SW.xml
    https://www.rightmove.co.uk/sitemap-properties-SW.xml
    https://www.rightmove.co.uk/sitemap-agents-ALL.xml
    '''
    
    start_urls = ['https://www.rightmove.co.uk/sitemap-properties-SW.xml']
    
    transaction_history_api_url_prefix = 'https://www.rightmove.co.uk/properties/api/soldProperty/transactionHistory/'

    def parse(self, response):
        for event, element in iterparse(BytesIO(response.body), tag='{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            print(element.text)
            if (element.text.startswith('https://www.rightmove.co.uk/property-for-sale/')):
                # if (element.text == 'https://www.rightmove.co.uk/property-for-sale/property-100177769.html'):
                yield response.follow(element.text, callback=self.parse_property)
                    # break
            element.clear()

    def parse_property(self, response):
        print('parse_property')
        match = re.search('\"deliveryPointId\"\:([0-9]+|null)', response.text)
        if match is not None:
            deliveryPointId = match.group(1)
            if deliveryPointId.isnumeric():
                yield response.follow(self.transaction_history_api_url_prefix + str(deliveryPointId), callback=self.parse_transaction_history)
            else:
                print(deliveryPointId)
        else:
            print("match is None")
                
    def parse_transaction_history(self, response):
        print('parse_transaction_history')
        print(response.body)

# %%
# import requests
# def xpath_ns(tree, expr):
#     "Parse a simple expression and prepend namespace wildcards where unspecified."
#     def qual(
#         n): return n if not n or ':' in n or '()' in n else '*[local-name() = "%s"]' % n
#     expr = '/'.join(qual(n) for n in expr.split('/'))
#     return tree.xpath(expr)


# url = "https://www.rightmove.co.uk/sitemap-outcodes-SW.xml"
# res = requests.get(url)
# xml = res.content
# # root = etree.fromstring(xml)

# for event, element in iterparse(BytesIO(xml), tag="{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
#     print(element.text)
#     element.clear()

# loc = xpath_ns(root, "//url/loc/text()")
# print(loc)
# namespace = [v for v in root.nsmap.values()]
# print(namespace)

# for element in root.iter():
#     if element.tag.endswith("loc"):
#         print(element.text)
    #     yield response.follow(element.text, callback=self.parse_property)
