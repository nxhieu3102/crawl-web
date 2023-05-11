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
import csv

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

def addLinkToCSV(fileLink, productLink):
    with open(fileLink,'a') as fd:
        writer = csv.writer(fd)
        writer.writerow(productLink)
        #fd.close()
        
def csvToList(fileLink):
    file = open(fileLink)
    csvreader = csv.reader(file)
    header = next(csvreader)  
    rows = []
    for row in csvreader:
        if row:
            rows.append(row)
    return rows

class TGDDLaptopLinkSpider(scrapy.Spider):
    name = 'TGDDLaptopLink'
    
    start_urls = [
        'https://www.thegioididong.com/laptop#c=44&o=17&pi=10'
    ]
    
    def parse(self, response):
        #instance = ProductItem()
        loaded = csvToList('./scraper/links/tgdd/laptop.csv')

        items = response.css('.__cate_44 > a.main-contain::attr(href)').extract()
        for item in items:
            # instance['ProductLink'] = 'https://thegioididong' + item
            # yield instance
            link = 'https://thegioididong' + item
            flag = True
            for i in loaded:
                if i[0] == link:
                    flag = False
                    break
            if flag:
                addLinkToCSV('./scraper/links/tgdd/laptop.csv',[link])

class TGDDLaptopDetailSpider(scrapy.Spider):
    loaded = csvToList('./scraper/links/tgdd/laptop.csv')
    name = 'TGDDLaptopDetail'
    index = 1
        
    start_urls = [
        loaded[0][0]
    ]
    
    def parse(self, response):
        
        
        instance = ProductItem()
        
        instance['ProductID'] = 'TGDDLAP' + str(self.index)
        #instance['ProductLink'] = self.loaded[self.index - 1]['ProductLink']
        instance['ProductLink'] = self.loaded[self.index - 1][0]
        
        instance['ProductName'] = response.css('section.detail h1::text').get()
        if instance['ProductName'] is None:
            instance['ProductName'] = 'Laptop '
            tmp = instance['ProductLink'].replace('https://www.thegioididong.com/laptop/','').split('-')
            for item in tmp:
                instance['ProductName'] += item.upper() + ' '
        
        instance['ImageLink'] = response.css('a.slider-item img::attr(src)').get()
        if not instance['ImageLink'].startswith('https:'):
            instance['ImageLink'] = 'https:' + instance['ImageLink']
        
        instance['ShopName'] = 'TGDD'
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
        if instance['SalePrice'] is not None and instance['SalePrice'].endswith('*'):
            instance['SalePrice'] = instance['SalePrice'].replace(' *','').strip()
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
        
        temp = response.xpath('/html/body/section[1]/div[3]/div[2]/div[1]/div/a[1]/text()').get()
        print(temp)
        if temp and 'gb' in temp.lower():
            tmp = response.xpath('/html/body/section[1]/div[3]/div[2]/div[1]/div/a[2]/@href').extract()
            print(tmp)
            if tmp:
                tmp = 'https://thegioididong' + tmp[0]
                print(tmp)
                flag = True
                for prodlink in self.loaded:
                    if prodlink[0] == tmp:
                        flag = False
                        break
                    
                if flag:
                    self.loaded.append([tmp])
                    addLinkToCSV('./scraper/links/tgdd/laptop.csv',[tmp])
                
        yield instance

        #print(self.loaded)
        if self.index < len(self.loaded):
            next_page = self.loaded[self.index][0]
        else: next_page = ''
        
        if self.index <= len(self.loaded) - 1:
            self.index += 1
            print(self.index)
            yield response.follow(next_page, callback = self.parse)#, headers = choice(CUSTOM_HEADERS))

class TGDDLaptopGamingSpider(scrapy.Spider):
    name = 'TGDDLaptopGaming'
    
    start_urls = [
        'https://www.thegioididong.com/laptop?g=laptop-gaming#c=44&p=37699&o=17&pi=2'
    ]
    
    def parse(self, response):
        instance = ProductItem()
        
        items = response.css('.__cate_44 > a.main-contain::attr(href)').extract()
        for item in items:
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = 'Gaming'
            instance['ProductLink'] = 'https://www.thegioididong.com' + item
            yield instance

class TGDDLaptopDohoakithuat(scrapy.Spider):
    name = 'TGDDLaptopDohoakithuat'
    
    start_urls = [
        'https://www.thegioididong.com/laptop?g=do-hoa-ky-thuat#c=44&p=81785&o=17&pi=3'
    ]
    
    def parse(self, response):
        instance = ProductItem()
        
        items = response.css('.__cate_44 > a.main-contain::attr(href)').extract()
        for item in items:
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = 'Thiết kế đồ hoạ'
            instance['ProductLink'] = 'https://www.thegioididong.com' + item
            yield instance

class TGDDLaptopHoctapvanphong(scrapy.Spider):
    name = 'TGDDLaptopHoctapvanphong'
    
    start_urls = [
        'https://www.thegioididong.com/laptop?g=hoc-tap-van-phong#c=44&p=37697&o=17&pi=7', 
    ]
    
    def parse(self, response):
        instance = ProductItem()
        
        items = response.css('.__cate_44 > a.main-contain::attr(href)').extract()
        for item in items:
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = 'Văn phòng'
            instance['ProductLink'] = 'https://www.thegioididong.com' + item
            yield instance

class TGDDPhoneLinkSpider(scrapy.Spider):
    name = 'TGDDPhoneLink'
    
    start_urls = [
        'https://www.thegioididong.com/dtdd#c=42&o=17&pi=5'
    ]
    
    def parse(self, response):
        instance = ProductItem()
        #categoryPage > div.container-productbox > ul > li:nth-child(1) > a.main-contain
        items = response.css('.__cate_44 > a.main-contain::attr(href)').extract()
        for item in items:
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = None
            instance['ProductLink'] = 'https://thegioididong' + item
            print(instance['ProductLink'])
            yield instance

class TGDDPhoneDetailSpider(scrapy.Spider):
    name = 'TGDDPhoneDetail'
    
    loaded = ''
    with open('./scraper/links/tgdd/phone.json') as value:
        loaded = json.load(value)
    index = 1
    
    start_urls = [
        loaded[0]['ProductLink'],
    ]
        
    def parse(self, response):        
        instance = ProductItem()
        
        instance['ProductID'] = 'TGDDPHONE' + str(self.index)
        instance['ProductLink'] = self.loaded[self.index - 1]['ProductLink']
        
        print(instance['ProductLink'])
        
        instance['ProductName'] = response.css('section.detail h1::text').get()
        if instance['ProductName'] is None:
            instance['ProductName'] = ''
            tmp = instance['ProductLink'].replace('https://www.thegioididong.com/dtdd/','').split('-')
            for item in tmp:
                instance['ProductName'] += item.upper() + ' '
            instance['ProductName'] = instance['ProductName'].strip()
        
        instance['ImageLink'] = response.css('a.slider-item img::attr(src)').get()
        if not instance['ImageLink'].startswith('https:'):
            instance['ImageLink'] = 'https:' + instance['ImageLink']
        
        instance['ShopName'] = 'TGDD'
        
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
        if instance['SalePrice'] is not None and instance['SalePrice'].endswith('*'):
            instance['SalePrice'] = instance['SalePrice'].replace(' *','').strip()
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
        
        #print(instance)
        
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
    name = 'TGDDTabletDetail'
    
    loaded = ''
    with open('./scraper/links/tgdd/tablet.json') as value:
        loaded = json.load(value)
    index = 1
    
    start_urls = [
        loaded[0]['ProductLink'],
    ]
        
    def parse(self, response):        
        instance = ProductItem()
        
        instance['ProductID'] = 'TGDDTABLET' + str(self.index)
        instance['ProductLink'] = self.loaded[self.index - 1]['ProductLink']
        
        print(instance['ProductLink'])
        
        instance['ProductName'] = response.css('section.detail h1::text').get()
        if instance['ProductName'] is None:
            instance['ProductName'] = ''
            tmp = instance['ProductLink'].replace('https://www.thegioididong.com/may-tinh-bang/','').split('-')
            for item in tmp:
                instance['ProductName'] += item.upper() + ' '
            instance['ProductName'] = instance['ProductName'].strip()
        
        instance['ImageLink'] = response.css('a.slider-item img::attr(src)').get()
        if instance['ImageLink'] is not None and not instance['ImageLink'].startswith('https:'):
            instance['ImageLink'] = 'https:' + instance['ImageLink']
        
        instance['ShopName'] = 'TGDD'
        
        instance['BrandName'] = ''
        if instance['ProductName']:
            brands = ['ipad' , 'samsung' , 'oppo' , 'xiaomi' ,
                  'nokia' , 'masstel', 'lenovo']
            
            for brand in brands:
                if brand.upper() in instance['ProductName'].upper():
                    if brand == 'ipad':
                        brand = 'APPLE'
                    instance['BrandName'] = brand.upper()
                    break
    
        instance['SalePrice'] = response.css('p.box-price-present::text').get()
        if instance['SalePrice'] is not None and instance['SalePrice'].endswith('*'):
            instance['SalePrice'] = instance['SalePrice'].replace(' *','').strip()
        tmp = response.css('p.box-price-old::text').get()
        if tmp is not None:
            instance['NormalPrice'] = tmp
        else: instance['NormalPrice'] = instance['SalePrice']
        
        instance['Type'] = 'Máy tính bảng'
        
        ConfigPattern = ["Dung lượng lưu trữ", "Màn hình", "Hệ điều hành", 
                          "Pin", "Camera sau", "Camera trước"]
        
        realName = ["Lưu trữ", "Màn hình", "Hệ điều hành", 
                    "Pin", "Camera sau", "Camera trước"]
        
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
        
        #print(instance)
        
        yield instance
        
        if self.index < len(self.loaded):
            next_page = self.loaded[self.index]['ProductLink']
        else: next_page = ''
        
        if self.index <= len(self.loaded) - 1:
            self.index += 1
            yield response.follow(next_page, callback = self.parse, headers = choice(CUSTOM_HEADERS))
