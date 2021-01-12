    # Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FdaScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()     
    import_alert = scrapy.Field()
    publication = scrapy.Field()
    type_alert = scrapy.Field()
    description_al = scrapy.Field()
    charge = scrapy.Field()
