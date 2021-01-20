# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from postcode.models import Postcode, db_connect, create_table


class SavePostcodesPipeline(object):
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
        postcode = Postcode()
        postcode.postcode = item['postcode']
        postcode.postcodeEncoded = item['postcodeEncoded']
        

        try:
            session.add(postcode)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item