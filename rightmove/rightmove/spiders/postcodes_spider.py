#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: michael
"""

import scrapy
from scrapy.loader import ItemLoader
from rightmove.items import PropertyItem
import orjson

class PropertiesSpider(scrapy.Spider):
    name = 'postcodes'
    # allowed_domains = ["rightmove.co.uk"]
    
    start_urls = []
    
    for i in range(100):
        start_urls.append(f'https://www.rightmove.co.uk/api/_search?locationIdentifier=POSTCODE%5E{i+1}&channel=BUY')
        

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
                loader.add_value('property_bedrooms', property['bedrooms'])
                loader.add_value('property_numberOfImages', property['numberOfImages'])
                loader.add_value('property_numberOfFloorplans', property['numberOfFloorplans'])
                loader.add_value('property_numberOfVirtualTours', property['numberOfVirtualTours'])
                
