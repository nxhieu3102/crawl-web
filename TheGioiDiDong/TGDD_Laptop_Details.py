import scrapy
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import Request
from random import choice
from apscheduler.schedulers.twisted import TwistedScheduler

CUSTOM_HEADERS = [
        {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        },
        {
            'User-Agent' : 'Mozilla/5.0 (Linux; Android 9; SM-T820 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.101 Safari/537.36 ANDROID_APP'
        },
        {
            'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Silk/85.3.5 like Chrome/85.0.4183.126 Safari/537.36"
        },
        {
            'User-Agent' : "Mozilla/5.0 (Linux; Android 10.0; X116L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        },
        {
            'User-Agent' : "Mozilla/5.0 (X11; U; U; Linux x86_64; nl-nl) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 Puffin/8.4.0.42081AP"
        },
        {
            'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.64 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
        }
    ]

class LaptopDetails(scrapy.Spider):
    name = 'LapTop'
    count = 0
    def start_requests(self):
        # print('hello')
        urls = ['https://www.thegioididong.com/laptop/asus-tuf-gaming-fx517zc-i5-hn077w'] #load url from links file
        for url in urls:
            headers = choice(CUSTOM_HEADERS)
            yield Request(url=url, headers=headers, callback=self.parse)
            # yield Request(url=url, headers=headers, callback=self.parse, meta={'download_delay': 120})
            # time.sleep(5)

    # price
    def getPrice(response):
        SalePrice = None
        NormalPrice = None
        temp = response.css('p.box-price-present::text').get()
        # print(temp)
        if temp == None:
            return [NormalPrice , SalePrice]
        
        SalePrice = temp
        NormalPrice = response.css('p.box-price-old::text').get()
        return [NormalPrice , SalePrice]
    
    #name
    def getName(response):
        return response.css('section.detail h1::text').get()

    # config
    def getConfig(response):
        realName = ["CPU", "RAM", "Lưu trữ", "Màn hình", 
                        "Hệ điều hành", "Đồ hoạ", "Pin", "Khối lượng"]
        ConfigPattern = ["CPU:", "RAM:", "Ổ cứng:", "Màn hình:",
                    "Hệ điều hành:", "Card màn hình:", "Pin:", "khối lượng"]
        #chua xong
        
        size = len(response.css('.parameter__list li'))

        item = {}

        for i in range(size):
            detailPath = f'.parameter__list li:nth-child({i+1}) div span::text'
            list = response.css(detailPath).extract()
            strList = ", ".join(list)

            attributePath = f'.parameter__list li:nth-child({i+1}) p::text'
            attribute = response.css(attributePath).get()

            configSize = len(ConfigPattern)
            for j in range(configSize):
                if ConfigPattern[j] in attribute:

                    if realName[j] == "Khối lượng":
                        strList = strList.split('-')[-1]
                        strList = strList.replace('Nặng', "").strip()

                    item[realName[j]] = strList
                    break

        return item

    # brandName
    def findBrand(s):
        brands = ['macbook' , 'asus' , 'hp' , 'lenovo' , 'acer' , 'dell' ,
                  'msi' , 'surface' , 'itel' , 'masstel' , 'chuwi' , 'lg']
        for brand in brands:
            if brand.upper() in s.upper():
                if brand == 'macbook':
                    brand = 'APPLE'
                return brand.upper()
        return None
    
    # image
    def getImage(response):
        img = 'None'
        img = response.css('a.slider-item img::attr(src)').get()
        # print('ec ec')
        # print(temp)
        return img

    #promotion
    def getPromotion(response):
        if response.css('div.divb-right') == None:
            return []
        
        size = len(response.css('div.divb-right'))
        list = []

        # for i in range(size):

        for p in response.css('div.divb-right p'):
            text = ''
            for node in p.css('*::text'):
                text += node.extract().strip()
            text = text.replace("(click xem chi tiết)" , "")
            list.append(text)
            # print(text)

        return list

    def parse(self, response):
        item = {}

        temp = LaptopDetails.getPrice(response)
        item['SalePrice'] = temp[1] #present price
        item['NormalPrice'] = temp[0] #old price
        if temp[1] == None:
            return
        

        LaptopDetails.count += 1
        item['ProductID'] = 'TGLAPTOP' + str(LaptopDetails.count)
        
        item['ImageLink'] = LaptopDetails.getImage(response)

        item['ProductName'] = LaptopDetails.getName(response)

        item['ShopName'] = 'TGDD'

        item['Type'] = 'Laptop'
        
        item['BrandName'] = LaptopDetails.findBrand(item['ProductName'])

        item['ConfigDetail'] = LaptopDetails.getConfig(response)

        item['PromotionDetail'] = LaptopDetails.getPromotion(response)

        item['ProductLink'] = response.url
        # item['FeatureDetail']

        print(item)

        
def solve():
    process = CrawlerProcess(get_project_settings())
    scheduler = TwistedScheduler()
    scheduler.add_job(process.crawl, 'interval', args = [LaptopDetails], seconds = 2)
    scheduler.start()
    process.start(False)

solve()

