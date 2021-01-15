# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class Property(Base):
    __tablename__ = "property"
    id = Column(Integer, primary_key=True)
    property_id = Column('property_id', Integer)
    bedrooms = Column('bedrooms', Integer)
    numberOfImages = Column('numberOfImages', Integer)
    numberOfFloorplans = Column('numberOfFloorplans', Integer)
    numberOfVirtualTours = Column('numberOfVirtualTours', Integer)
    summary = Column('summary', Text())
    displayAddress = Column('displayAddress', Text())
    countryCode = Column('countryCode', Text())
    location_latitude = Column('location_latitude', Float)
    location_longitude = Column('location_longitude', Float)
    propertySubType = Column('propertySubType', Text())
    listingUpdate_reason = Column('listingUpdate_reason', Text())
    listingUpdate_date = Column('listingUpdate_date', Text())
    premiumListing = Column('premiumListing', Integer)
    featuredProperty = Column('featuredProperty', Integer)
    price_amount = Column('price_amount', Integer)
    price_currencyCode = Column('price_currencyCode', Text())
    price_frequency = Column('price_frequency', Text())
    distance = Column('distance', Text())
    transactionType = Column('transactionType', Text())
    commercial = Column('commercial', Integer)
    development = Column('development', Integer)
    residential = Column('residential', Integer)
    students = Column('students', Integer)
    auction = Column('auction', Integer)
    feesApply = Column('feesApply', Integer)
    feesApplyText = Column('feesApplyText', Text())
    propertyUrl = Column('propertyUrl', Text())
    contactUrl = Column('contactUrl', Text())
    staticMapUrl = Column('staticMapUrl', Text())
    channel = Column('channel', Text())
    firstVisibleDate = Column('firstVisibleDate', Text())
    heading = Column('heading', Text())
    displayStatus = Column('displayStatus', Text())
    formattedBranchName = Column('formattedBranchName', Text())
    addedOrReduced = Column('addedOrReduced', Text())
    isRecent = Column('isRecent', Integer)
    formattedDistance = Column('formattedDistance', Text())
    propertyTypeFullDescription = Column('propertyTypeFullDescription', Text())
    enhancedListing = Column('enhancedListing', Integer)
    hasBrandPlus = Column('hasBrandPlus', Integer)
    
    soldPropertyTransactionHistories = Column('soldPropertyTransactionHistories', Text())



# Association Table for Many-to-Many relationship between Quote and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
# quote_tag = Table('quote_tag', Base.metadata,
#     Column('quote_id', Integer, ForeignKey('quote.id')),
#     Column('tag_id', Integer, ForeignKey('tag.id'))
# )


# class Quote(Base):
#     __tablename__ = "quote"

#     id = Column(Integer, primary_key=True)
#     quote_content = Column('quote_content', Text())
#     author_id = Column(Integer, ForeignKey('author.id'))  # Many quotes to one author
#     tags = relationship('Tag', secondary='quote_tag',
#         lazy='dynamic', backref="quote")  # M-to-M for quote and tag


# class Author(Base):
#     __tablename__ = "author"

#     id = Column(Integer, primary_key=True)
#     name = Column('name', String(50), unique=True)
#     birthday = Column('birthday', DateTime)
#     bornlocation = Column('bornlocation', String(150))
#     bio = Column('bio', Text())
#     quotes = relationship('Quote', backref='author')  # One author to many Quotes


# class Tag(Base):
#     __tablename__ = "tag"

#     id = Column(Integer, primary_key=True)
#     name = Column('name', String(30), unique=True)
#     quotes = relationship('Quote', secondary='quote_tag',
#         lazy='dynamic', backref="tag")  # M-to-M for quote and tag