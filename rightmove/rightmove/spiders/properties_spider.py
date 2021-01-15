#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: michael
"""

import scrapy
from scrapy.loader import ItemLoader
from rightmove.items import PropertyItem
import orjson
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
    
    prices = [0, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000,
              125000, 130000, 140000, 150000, 160000, 170000, 175000,
              180000, 190000, 200000, 210000, 220000, 230000, 240000,
              250000, 260000, 270000, 280000, 290000, 300000, 325000,
              350000, 375000, 400000, 425000, 450000, 475000, 500000,
              550000, 600000, 650000, 700000, 800000, 900000, 1000000,
              1250000, 1500000, 1750000, 2000000, 2500000, 3000000,
              4000000, 5000000, 7500000, 10000000, 15000000, 20000001]
    
    sw19_buy_url = 'https://www.rightmove.co.uk/api/_search?locationIdentifier=OUTCODE%5E2505&channel=BUY'
    
    start_urls = []
    

    for i in range(len(prices)-1):
        start_urls.append(f'{sw19_buy_url}&minPrice={prices[i]}&maxPrice={prices[i+1]-1}')
    
    
    print(start_urls)
    
    
    transaction_history_api_url_prefix = 'https://www.rightmove.co.uk/properties/api/soldProperty/transactionHistory/'

    

    def parse(self, response):
        try:
            index = response.meta['index']
            original_url = response.meta['original_url']
        except KeyError:     
            index = 0
            original_url = response.request.url
            
        json_object = orjson.loads(response.body)
        
        result_count = int(json_object['resultCount'])
        if result_count - index > 24:
            new_index = index + 24
            yield response.follow(f'{original_url}&index={new_index}', self.parse, meta={'index': new_index, 
                                                                                         'original_url': original_url})
        
        properties = json_object['properties']
        if not len(properties) == 0:
            for property in properties:
                loader = ItemLoader(item=PropertyItem())
                loader.add_value('property_id', property['id'])
                loader.add_value('bedrooms', property['bedrooms'])
                loader.add_value('numberOfImages', property['numberOfImages'])
                loader.add_value('numberOfFloorplans', property['numberOfFloorplans'])
                loader.add_value('numberOfVirtualTours', property['numberOfVirtualTours'])
                loader.add_value('summary', property['summary'])
                loader.add_value('displayAddress', property['displayAddress'])
                loader.add_value('countryCode', property['countryCode'])
                loader.add_value('location_latitude', property['location']['latitude'])
                loader.add_value('location_longitude', property['location']['longitude'])
                loader.add_value('propertySubType', property['propertySubType'])
                loader.add_value('listingUpdate_reason', property['listingUpdate']['listingUpdateReason'])
                loader.add_value('listingUpdate_date', property['listingUpdate']['listingUpdateDate'])
                loader.add_value('premiumListing', property['premiumListing'])
                loader.add_value('featuredProperty', property['featuredProperty'])
                loader.add_value('price_amount', property['price']['amount'])
                loader.add_value('price_currencyCode', property['price']['currencyCode'])
                loader.add_value('price_frequency', property['price']['frequency'])
                try:
                    loader.add_value('distance', property['distance'])
                except KeyError:
                    pass
                loader.add_value('transactionType', property['transactionType'])
                loader.add_value('commercial', property['commercial'])
                loader.add_value('development', property['development'])
                loader.add_value('residential', property['residential'])
                loader.add_value('students', property['students'])
                loader.add_value('auction', property['auction'])
                loader.add_value('feesApply', property['feesApply'])
                try:
                    loader.add_value('feesApplyText', property['feesApplyText'])
                except KeyError:
                    pass
                loader.add_value('propertyUrl', property['propertyUrl'])
                loader.add_value('contactUrl', property['contactUrl'])
                try:
                    loader.add_value('staticMapUrl', property['staticMapUrl'])
                except KeyError:
                    pass
                loader.add_value('channel', property['channel'])
                loader.add_value('firstVisibleDate', property['firstVisibleDate'])
                loader.add_value('heading', property['heading'])
                loader.add_value('displayStatus', property['displayStatus'])
                loader.add_value('formattedBranchName', property['formattedBranchName'])
                loader.add_value('addedOrReduced', property['addedOrReduced'])
                loader.add_value('isRecent', property['isRecent'])
                loader.add_value('formattedDistance', property['formattedDistance'])
                loader.add_value('propertyTypeFullDescription', property['propertyTypeFullDescription'])
                loader.add_value('enhancedListing', property['enhancedListing'])
                loader.add_value('hasBrandPlus', property['hasBrandPlus'])

                
                property_item = loader.load_item()
                
                yield response.follow(f'https://www.rightmove.co.uk{property["propertyUrl"]}', callback=self.parse_property, meta={'property_item': property_item})


    def parse_property(self, response):
        property_item = response.meta['property_item']
        
        match = re.search('\"deliveryPointId\"\:([0-9]+|null)', response.text)
        if match is not None:
            deliveryPointId = match.group(1)
            if deliveryPointId.isnumeric():
                yield response.follow(self.transaction_history_api_url_prefix + str(deliveryPointId), callback=self.parse_transaction_history, meta={'property_item': property_item})
            else:
                print(deliveryPointId)
        else:
            print('match is None')
                
    def parse_transaction_history(self, response):
        property_item = response.meta['property_item']

        loader = ItemLoader(item=property_item, response=response)
        loader.add_value('soldPropertyTransactionHistories', response.body)
        yield loader.load_item()

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
