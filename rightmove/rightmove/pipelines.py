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
        property.bedrooms = item['property_bedrooms']
        property.numberOfImages = item['property_numberOfImages']
        property.numberOfFloorplans = item['property_numberOfFloorplans']
        property.numberOfVirtualTours = item['property_numberOfVirtualTours']

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