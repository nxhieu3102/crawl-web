from scraper.spiders.PhongVu import PVLaptopDetailSpider, PVLaptopLinkSpider
from scraper.spiders.FPTShop import FPTLaptopLinkSpider
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from apscheduler.schedulers.twisted import TwistedScheduler

from scraper import settings as my_settings

crawler_settings = Settings()
crawler_settings.setmodule(my_settings)
process = CrawlerProcess(settings=crawler_settings)
scheduler = TwistedScheduler()

#Phong Vu scheduler 
scheduler.add_job(process.crawl, 'interval', args = [PVLaptopLinkSpider], seconds = 120)
scheduler.start()
process.start(False)
