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

class DTDetails(scrapy.Spider):
    name = 'DienThoai'
    count = 0
    def start_requests(self):
        # print('hello')
        urls = ['https://www.thegioididong.com/dtdd/nokia-g22']
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
        ConfigPattern = ["Dung lượng lưu trữ", "Màn hình", "Hệ điều hành", 
                          "Pin", "Camera sau", "Camera trước"]
        
        realName = ["Lưu trữ", "Màn hình", "Hệ điều hành", 
                    "Pin", "Camera sau", "Camera trước"]
        
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
                    item[realName[j]] = strList
                    break

        return item

    # brandName
    def findBrand(s):
        brands = ['iphone' , 'samsung' , 'oppo' , 'xiaomi' , 'vivo' , 'realme' , 
                  'nokia' , 'tcl' , 'mobell' , 'itel' , 'masstel']
        for brand in brands:
            if brand.upper() in s.upper():
                if brand == 'iphone':
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
            print(text)
            list.append(text)

        return list

    def parse(self, response):
        item = {}
        #hinh nhu thieu rating

        temp = DTDetails.getPrice(response)
        item['SalePrice'] = temp[1] #present price
        item['NormalPrice'] = temp[0] #old price
        if temp[1] == None:
            return
        

        DTDetails.count += 1
        item['ProductID'] = 'TGPHONE' + str(DTDetails.count)
        
        item['ImageLink'] = DTDetails.getImage(response)

        item['ProductName'] = DTDetails.getName(response)

        item['ShopName'] = 'TGDD'

        item['Type'] = 'Điện thoại'
        
        item['BrandName'] = DTDetails.findBrand(item['ProductName'])

        item['ConfigDetail'] = DTDetails.getConfig(response)

        item['PromotionDetail'] = DTDetails.getPromotion(response)

        item['ProductLink'] = response.meta.get('url')
        # item['FeatureDetail']
        
    

        print(item)

        


def solve():
    process = CrawlerProcess(get_project_settings())
    scheduler = TwistedScheduler()
    scheduler.add_job(process.crawl, 'interval', args = [DTDetails], seconds = 2)
    scheduler.start()
    process.start(False)

solve()


# <a href="javascript:void(0)" class="slider-item" data-gallery-id="featured-images-gallery" data-color-id="0" data-picture-id="235390" data-video-id data-index="0" data-time="0"> flex
#     <img src="https://cdn.tgdd.vn/Products/Images/42/303937/Slider/nokia-g22-tong-auan-lc-1020x570.png" alt="Nokia G22" width="710" height="394">
# </a>
