# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from rightmove.models import Property, db_connect, create_table


class SaveQuotesPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        property = Property()
        property.property_id = item['property_id']
        property.bedrooms = item['bedrooms']
        property.numberOfImages = item['numberOfImages']
        property.numberOfFloorplans = item['numberOfFloorplans']
        property.numberOfVirtualTours = item['numberOfVirtualTours']
        property.summary = item['summary']
        property.displayAddress = item['displayAddress']
        property.countryCode = item['countryCode']
        property.location_latitude = item['location_latitude']
        property.location_longitude = item['location_longitude']
        property.propertySubType = item['propertySubType']
        property.listingUpdate_reason = item['listingUpdate_reason']
        property.listingUpdate_date = item['listingUpdate_date']
        property.premiumListing = item['premiumListing']

        try:
            session.add(property)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item


class DuplicatesPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        exist_property = session.query(Property).filter_by(property_id = item["property_id"]).first()
        if exist_property is not None:  # the current quote exists
            raise DropItem("Duplicate item found: %s" % item["property_id"])
            session.close()
        else:
            return item
            session.close()