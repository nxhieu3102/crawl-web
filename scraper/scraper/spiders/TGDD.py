import scrapy
from ..items import ProductItem
import json
from random import choice
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import re

options = Options()
options.add_argument("--headless")

CUSTOM_HEADERS = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    },
    {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    },
    {
        "User-Agent": "Mozilla/5.0 (PlayStation 4 3.11) AppleWebKit/537.73 (KHTML, like Gecko)",
    },
    {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus Player Build/MMB29T)",
    },
    {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    },
]

class TGDDLaptopLinkSpider(scrapy.Spider):
    name = 'TGDDLaptopLink'
    
    start_urls = [
        'https://www.thegioididong.com/laptop#c=44&o=17&pi=10'
    ]
    
    def parse(self, response):
        instance = ProductItem()
        
        items = response.css('.__cate_44 > a.main-contain::attr(href)').extract()
        for item in items:
            instance['ProductLink'] = 'https://thegioididong' + item
            yield instance

class TGDDLaptopDetailSpider(scrapy.Spider):
    name = 'TGDDLaptopDetail'
    
    loaded = ''
    with open('./scraper/links/TGDDLaptopLink.json') as value:
        loaded = json.load(value)
    index = 1
    
    start_urls = [
        loaded[0]['ProductLink'],
    ]
        
    def parse(self, response):
        
        print(response.url)
        
        instance = ProductItem()
        
        instance['ProductID'] = 'TGDDLAP' + str(self.index)
        instance['ProductLink'] = self.loaded[self.index - 1]['ProductLink']
        
        instance['ProductName'] = response.css('section.detail h1::text').get()
        if instance['ProductName'] is None:
            instance['ProductName'] = 'Laptop'
            tmp = instance['ProductLink'].replace('https://www.thegioididong.com/laptop/','').split('-')
            for item in tmp:
                instance['ProductName'] += item.upper() + ' '
        
        instance['ImageLink'] = response.css('a.slider-item img::attr(src)').get()
        if not instance['ImageLink'].startswith('https:'):
            instance['ImageLink'] = 'https:' + instance['ImageLink']
        
        
        instance['BrandName'] = ''
        
        if instance['ProductName']:
            brands = ['macbook' , 'asus' , 'hp' , 'lenovo' , 'acer' , 'dell' ,
                    'msi' , 'surface' , 'itel' , 'masstel' , 'chuwi' , 'lg']
            for brand in brands:
                if brand.upper() in instance['ProductName'].upper():
                    if brand == 'macbook':
                        brand = 'APPLE'
                    instance['BrandName'] = brand.upper()
                    break
        
        instance['SalePrice'] = response.css('p.box-price-present::text').get()
        tmp = response.css('p.box-price-old::text').get()
        if tmp is not None:
            instance['NormalPrice'] = tmp
        else: instance['NormalPrice'] = instance['SalePrice']
        
        instance['Type'] = 'Máy tính cá nhân'
        
        realName = ["CPU", "RAM", "Lưu trữ", "Màn hình", 
                        "Hệ điều hành", "Đồ hoạ", "Pin", "Khối lượng"]
        ConfigPattern = ["CPU:", "RAM:", "Ổ cứng:", "Màn hình:",
                    "Hệ điều hành:", "Card màn hình:", "Pin:", "khối lượng"]
        
        size = len(response.css('.parameter__list li'))

        instance['ConfigDetail'] = {}

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

                    instance['ConfigDetail'][realName[j]] = strList
                    break
        
        instance['PromotionDetail'] = []
    
        size = len(response.css('div.divb-right'))

        for p in response.css('div.divb-right p'):
            text = ''
            for node in p.css('*::text'):
                text += node.extract().strip()
            text = text.replace("(click xem chi tiết)" , "")
            instance['PromotionDetail'].append(text)

        instance['FeatureDetail'] = []
                
        yield instance
        
        if self.index < len(self.loaded):
            next_page = self.loaded[self.index]['ProductLink']
        else: next_page = ''
        
        if self.index <= len(self.loaded) - 1:
            self.index += 1
            yield response.follow(next_page, callback = self.parse, headers = choice(CUSTOM_HEADERS))

class TGDDLaptopGamingSpider(scrapy.spider):
    pass

class TGDDLaptopDohoakithuat(scrapy.Spider):
    pass

class TGDDLaptopHoctapvanphong(scrapy.Spider):
    pass

class TGDDPhoneLinkSpider(scrapy.Spider):
    pass

class TGDDPhoneDetailSpider(scrapy.Spider):
    name = 'TGDDPhoneDetail'
    
    loaded = ''
    with open('./scraper/links/TGDDPhoneLink.json') as value:
        loaded = json.load(value)
    index = 1
    
    start_urls = [
        loaded[0]['ProductLink'],
    ]
        
    def parse(self, response):        
        instance = ProductItem()
        
        instance['ProductID'] = 'TGDDPHONE' + str(self.index)
        instance['ProductLink'] = self.loaded[self.index - 1]['ProductLink']
        
        instance['ProductName'] = response.css('section.detail h1::text').get()
        if instance['ProductName'] is None:
            tmp = instance['ProductLink'].replace('https://www.thegioididong.com/laptop/','').split('-')
            for item in tmp:
                instance['ProductName'] += item.upper() + ' '
        
        instance['ImageLink'] = response.css('a.slider-item img::attr(src)').get()
        if not instance['ImageLink'].startswith('https:'):
            instance['ImageLink'] = 'https:' + instance['ImageLink']
        
        
        instance['BrandName'] = ''
        if instance['ProductName']:
            brands = ['iphone' , 'samsung' , 'oppo' , 'xiaomi' , 'vivo' , 'realme' , 
                  'nokia' , 'tcl' , 'mobell' , 'itel' , 'masstel']
            
            for brand in brands:
                if brand.upper() in instance['ProductName'].upper():
                    if brand == 'iphone':
                        brand = 'APPLE'
                    instance['BrandName'] = brand.upper()
                    break
    
        instance['SalePrice'] = response.css('p.box-price-present::text').get()
        tmp = response.css('p.box-price-old::text').get()
        if tmp is not None:
            instance['NormalPrice'] = tmp
        else: instance['NormalPrice'] = instance['SalePrice']
        
        instance['Type'] = 'Điện thoại'
        
        ConfigPattern = ["Dung lượng lưu trữ", "Màn hình", "Hệ điều hành", 
                          "Pin", "Camera sau", "Camera trước"]
        
        realName = ["Lưu trữ", "Màn hình", "Hệ điều hành", 
                    "Pin", "Camera sau", "Camera trước"]
        
        size = len(response.css('.parameter__list li'))

        instance['ConfigDetail'] = {}
        
        size = len(response.css('.parameter__list li'))

        for i in range(size):
            detailPath = f'.parameter__list li:nth-child({i+1}) div span::text'
            list = response.css(detailPath).extract()
            strList = ", ".join(list)

            attributePath = f'.parameter__list li:nth-child({i+1}) p::text'
            attribute = response.css(attributePath).get()

            configSize = len(ConfigPattern)
            for j in range(configSize):
                if ConfigPattern[j] in attribute:
                    instance['ConfigDetail'][realName[j]] = strList
                    break


        
        instance['PromotionDetail'] = []
    
        size = len(response.css('div.divb-right'))

        for p in response.css('div.divb-right p'):
            text = ''
            for node in p.css('*::text'):
                text += node.extract().strip()
            text = text.replace("(click xem chi tiết)" , "")
            instance['PromotionDetail'].append(text)

        instance['FeatureDetail'] = []
                
        yield instance
        
        if self.index < len(self.loaded):
            next_page = self.loaded[self.index]['ProductLink']
        else: next_page = ''
        
        if self.index <= len(self.loaded) - 1:
            self.index += 1
            yield response.follow(next_page, callback = self.parse, headers = choice(CUSTOM_HEADERS))

    
class TGDDTabletLinkSpider(scrapy.Spider):
    pass

class TGDDTabletDetailSpider(scrapy.Spider):
    pass