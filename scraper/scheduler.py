from scraper.spiders.PhongVu import PVLaptopLinkSpider, PVLaptopDetailSpider, PVLaptopDoanhnghiepSpider, PVLaptopDoanhnhanSpider, PVLaptopGaming, PVLaptopHocsinhsinhvien, PVLaptopVanphong, PVLaptopThietkedohoa
from scrapy.crawler import CrawlerProcess
from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.settings import Settings

from scraper import settings as my_settings

crawler_settings = Settings()
crawler_settings.setmodule(my_settings)
process = CrawlerProcess(settings=crawler_settings)
scheduler = TwistedScheduler()

#Phong Vu scheduler 
scheduler.add_job(process.crawl, 'interval', args = [PVLaptopDetailSpider], seconds = 86400)
scheduler.add_job(process.crawl, 'interval', args = [PVLaptopDoanhnghiepSpider], seconds = 604800)
scheduler.add_job(process.crawl, 'interval', args = [PVLaptopDoanhnhanSpider], seconds = 604810)
scheduler.add_job(process.crawl, 'interval', args = [PVLaptopGaming], seconds = 604820)
scheduler.add_job(process.crawl, 'interval', args = [PVLaptopHocsinhsinhvien], seconds = 604830)
scheduler.add_job(process.crawl, 'interval', args = [PVLaptopVanphong], seconds = 604840)
scheduler.add_job(process.crawl, 'interval', args = [PVLaptopThietkedohoa], seconds = 604850)

scheduler.start()
process.start(False)
