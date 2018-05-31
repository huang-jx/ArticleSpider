# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class ArticleItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


class ArticlespiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    create_time = scrapy.Field()
    article_kind = scrapy.Field()
    praise_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    commant_nums = scrapy.Field()
    #content = scrapy.Field()
    author_name = scrapy.Field()



