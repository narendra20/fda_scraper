import requests
import scrapy
from ..items import FdaScraperItem
from lxml import html
from scrapy.http import HtmlResponse
from scrapy import Selector
from inline_requests import inline_requests
from scrapy.http import Request
import re
import dateparser
from datetime import datetime
from datetime import date
import calendar

class QuotesSpider(scrapy.Spider):
    name = "jobs"
    start_urls = [
        'https://www.accessdata.fda.gov/cms_ia/',
    ]
    @inline_requests
    def parse(self, response):
        max_pages = yield scrapy.Request('https://www.accessdata.fda.gov/cms_ia/iapublishdate.html', dont_filter = True)
        pages = max_pages.xpath('.//td[4]/a/@href').getall()
        print(len(pages))
        items = FdaScraperItem()
        for projects in pages:
            try:
                job = yield Request('https://www.accessdata.fda.gov/cms_ia/'+projects, dont_filter=True)
                if job.xpath('//*[@id="mp-pusher"]/div/div/div/div/div[3]/div/div[1]').get() != None:
                    import_alert = job.xpath('//*[@id="mp-pusher"]/div/div/div/div/div[3]/div/div[1]/text()').get()
                    # import_alert = import_alert.replace(' # ', '')
                else:
                    import_alert = ""
                if job.xpath('//*[@id="mp-pusher"]/div/div/div/div/div[3]/div/div[2]').get() != None:
                    publication = job.xpath('//*[@id="mp-pusher"]/div/div/div/div/div[3]/div/div[2]/text()').get()
                else:
                    publication = ""
                # last_date_of_update = dateparser.parse(publication).strftime("%Y-%m-%d")
                # last_date_of_update = datetime.strptime(last_date_of_update, "%Y-%m-%d").date()
                # if last_date_of_update >  datetime.now().date():
                #     raise SystemExit('All projects scraped until {}'.format(datetime.today()))
                if job.xpath('//*[@id="mp-pusher"]/div/div/div/div/div[3]/div/div[3]').get() != None:
                    type_alert = job.xpath('//*[@id="mp-pusher"]/div/div/div/div/div[3]/div/div[3]/text()').get()
                else:
                    type_alert = ""
                if job.xpath('//*[@id="mp-pusher"]/div/div/div/div/div[3]/div/div[4]').get() != None:
                    description_al = job.xpath('//*[@id="mp-pusher"]/div/div/div/div/div[3]/div/div[4]/text()').get()
                else:
                    description_al = ""
                # if job.xpath('//*[@id="mp-pusher"]/div/div/div/div/div[3]/div/div[8]/descendant-or-self::text()').get() != None:
                #     charge = job.xpath('//*[@id="mp-pusher"]/div/div/div/div/div[3]/div/div[8]/descendant-or-self::text()').getall()
                # else:
                #     charge = ""

                items['import_alert'] = import_alert
                items['publication'] = publication
                items['type_alert'] = type_alert
                items['description_al'] = description_al
                # items['charge'] = charge

                yield items
            except:
                pass