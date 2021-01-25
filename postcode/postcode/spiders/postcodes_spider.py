#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: michael
"""

import scrapy
from scrapy.loader import ItemLoader
from postcode.items import PostcodeItem
import re

class PostcodesSpider(scrapy.Spider):
    name = 'postcodes'
    # allowed_domains = ["rightmove.co.uk"]
    
    start_urls = []
    
    for i in range(1):
        start_urls.append(f'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=POSTCODE%5E{i+1+1753751}')
        

    def parse(self, response):
        title = response.xpath('/html/head/title/text()').get()
        match = re.match('Properties For Sale in (.*?) (.*?) | (.*?)', title)
        try:
            postcode = match.group(1)+" "+match.group(2)
        except:
            pass
        url = response.request.url
        match2 = re.match('.*?POSTCODE%5E(.*)', url)
        postcodeEncoded = match2.group(1)
        
        
        loader = ItemLoader(item=PostcodeItem())
        loader.add_value('postcode', postcode)
        loader.add_value('postcodeEncoded', postcodeEncoded)
        
        yield loader.load_item()

    
# #%%
# import MySQLdb
# import MySQLdb.cursors
# conn = MySQLdb.connect(host='localhost', db='uk_property', 
#                        user='root', passwd='P@ssw0rd',
#                        cursorclass=MySQLdb.cursors.DictCursor)

# postcode_dict = dict()
# try:
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT * FROM postcode")
#         db_nodes = cursor.fetchall()
 
#         for node in db_nodes:
#             postcode_dict[node['postcode']] = node['postcodeEncoded']
            
# finally:
#     conn.close()
    
# print(postcode_dict)