# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TopdevItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class JobItem(scrapy.Item):
   title = scrapy.Field()
   full_address = scrapy.Field()
   company_name = scrapy.Field()
   detail_url = scrapy.Field()
   job_level = scrapy.Field()
   skills = scrapy.Field()
   job_type = scrapy.Field()
   salary = scrapy.Field()
