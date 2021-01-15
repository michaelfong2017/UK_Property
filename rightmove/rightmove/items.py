# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
# from scrapy.loader.processors import MapCompose, TakeFirst
# from datetime import datetime


class PropertyItem(Item):
    property_id = Field()
    bedrooms = Field()
    numberOfImages = Field()
    numberOfFloorplans = Field()
    numberOfVirtualTours = Field()
    summary = Field()
    displayAddress = Field()
    countryCode = Field()
    location_latitude = Field()
    location_longitude = Field()
    propertySubType = Field()
    listingUpdate_reason = Field()
    listingUpdate_date = Field()
    premiumListing = Field()
    featuredProperty = Field()
    price_amount = Field()
    price_currencyCode = Field()
    price_frequency = Field()
    distance = Field()
    transactionType = Field()
    commercial = Field()
    development = Field()
    residential = Field()
    students = Field()
    auction = Field()
    feesApply = Field()
    feesApplyText = Field()
    propertyUrl = Field()
    contactUrl = Field()
    staticMapUrl = Field()
    channel = Field()
    firstVisibleDate = Field()
    heading = Field()
    displayStatus = Field()
    formattedBranchName = Field()
    addedOrReduced = Field()
    isRecent = Field()
    formattedDistance = Field()
    propertyTypeFullDescription = Field()
    enhancedListing = Field()
    hasBrandPlus = Field()
    
    soldPropertyTransactionHistories = Field()


# def remove_quotes(text):
#     # strip the unicode quotes
#     text = text.strip(u'\u201c'u'\u201d')
#     return text


# def convert_date(text):
#     # convert string March 14, 1879 to Python date
#     return datetime.strptime(text, '%B %d, %Y')


# def parse_location(text):
#     # parse location "in Ulm, Germany"
#     # this simply remove "in ", you can further parse city, state, country, etc.
#     return text[3:]

# class QuoteItem(Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     quote_content = Field(
#         input_processor=MapCompose(remove_quotes),
#         # TakeFirst return the first value not the whole list
#         output_processor=TakeFirst()
#         )
#     author_name = Field(
#         input_processor=MapCompose(str.strip),
#         output_processor=TakeFirst()
#         )
#     author_birthday = Field(
#         input_processor=MapCompose(convert_date),
#         output_processor=TakeFirst()
#     )
#     author_bornlocation = Field(
#         input_processor=MapCompose(parse_location),
#         output_processor=TakeFirst()
#     )
#     author_bio = Field(
#         input_processor=MapCompose(str.strip),
#         output_processor=TakeFirst()
#         )
#     tags = Field()
