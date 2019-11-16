# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AlltownriItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    home_id = scrapy.Field()
    name = scrapy.Field()
    availability = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()
    country = scrapy.Field()
    postal_code = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    bed = scrapy.Field()
    bath = scrapy.Field()
    status = scrapy.Field()
    mls_num = scrapy.Field()
    property_type = scrapy.Field()
    listing_type = scrapy.Field()
    build_year = scrapy.Field()
    size = scrapy.Field()
    