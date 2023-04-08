import scrapy
from ..items import ProductItem
import json
#from store.models 
#scrapy crawl LaptopLink -o name.json
class LaptopLinkSpider(scrapy.Spider):
    name = 'PVLapLink'
    page_number = 2
    start_urls = [
        'https://phongvu.vn/c/laptop?page=1'
    ]
    
    def parse(self, response):
        
        instance = ProductItem()
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()
    
        for item in items:
            instance['ProductLink'] = item
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?page=' + str(self.page_number)
        if self.page_number <= 1:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)

 
class LaptopDetailSpider(scrapy.Spider):
    loaded = ''
    with open('./scraper/links/PVLapLink.json') as value:
        loaded = json.load(value)
    
    print(len(loaded))
    
    name = 'PVLapDetail'
    index = 1
    
    start_urls = [
        'https://phongvu.vn' + loaded[0]['ProductLink']
    ]
        
    def parse(self, response):
        
        instance = ProductItem()
        
        instance['ProductID'] = 'PVLAP' + str(self.index)
        instance['ProductName'] = response.css('.css-4kh4rf::text').extract()[0]
        
        instance['BrandName'] = response.css('.css-n67qkj::text').extract()[0]
        instance['ShopName'] = 'PhongVu'
        
        instance['ImageLink'] = response.css('.css-j4683g img::attr(src)').extract()[0]
        instance['ProductLink'] = 'https://phongvu.vn' + self.loaded[self.index - 1]['ProductLink']

        #instance['Brand'] = response.css('.css-n67qkj::text').extract()[0]
        instance['SalePrice'] = response.css('.css-1q5zfcu .att-product-detail-latest-price::text').extract()[0]
        
        temp = response.css('.css-1q5zfcu .att-product-detail-retail-price::text').extract()
        if len(temp) == 0:
            instance['NormalPrice'] = instance['SalePrice']
        else: instance['NormalPrice'] = temp[0]
       
        instance['ConfigDetail'] = response.css('.css-17aam1::text').extract()
        if len(instance['ConfigDetail']) == 0:
            instance['ConfigDetail'] = response.css('.css-17aam1 p::text').extract()
        #instance['Link'] = 'https://phongvu.vn' + self.loaded[self.index - 1]['ProductLink']
        instance['Type'] = 'Máy tính cá nhân'
        
        temp = response.css('.css-hr6z5n::text').extract()
        if len(temp) == 0:
            instance['PromotionDetail'] = ''
        else: instance['PromotionDetail'] = temp
        
        instance['FeatureDetail'] = ''
        
        print(instance)
        yield instance
        
        if self.index < len(self.loaded):
            next_page = 'https://phongvu.vn' + self.loaded[self.index]['ProductLink']
        else: next_page = ''
        
        if self.index <= len(self.loaded) - 1:
            self.index += 1
            yield response.follow(next_page, callback = self.parse)
            
'''
class PhoneLinkSpider(scrapy.Spider):
    name = 'PhoneLink'
    start_urls = [
        'https://phongvu.vn/c/phone-dien-thoai'
    ]
    
    def parse(self, response):
        
        instance = PhongvuItem()
        
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()
        
        for item in items:
            instance['Link'] = item
            
            yield instance
        
class PhoneDetailSpider(scrapy.Spider):
    loaded = ''
    with open('PhoneLink.json') as value:
        loaded = json.load(value)
    
    name = 'PhoneDetail'
    index = 1
    
    start_urls = [
        'https://phongvu.vn' + loaded[0]['ProductLink']
    ]
        
    def parse(self, response):
        
        instance = PhongvuItem()
        
        instance['ID'] = 'PVPHONE' + str(self.index)
        
        instance['Name'] = response.css('.css-4kh4rf::text').extract()[0]
        instance['Img'] = response.css('.css-j4683g img::attr(src)').extract()[0]
        instance['Brand'] = response.css('.css-n67qkj::text').extract()[0]
        instance['Sale'] = response.css('.css-1q5zfcu .att-product-detail-latest-price::text').extract()[0]
        
        temp = response.css('.css-1q5zfcu .att-product-detail-retail-price::text').extract()
        if len(temp) == 0:
            instance['Price'] = instance['Sale']
        else: instance['Price'] = temp[0]

        instance['Config'] = response.css('.css-17aam1::text').extract()
        if len(instance['Config']) == 0:
            instance['Config'] = response.css('.css-17aam1 p::text').extract()
        instance['Link'] = 'https://phongvu.vn' + self.loaded[self.index - 1]['ProductLink']
        
        yield instance
        
        if self.index < len(self.loaded):
            next_page = 'https://phongvu.vn' + self.loaded[self.index]['ProductLink']
        else: next_page = ''
        
        if self.index <= len(self.loaded) - 1:
            self.index += 1
            yield response.follow(next_page, callback = self.parse)
    
class LapFeatureSpider(scrapy.Spider):
    
    features = {
        'Doanh nghiệp': [5, 26698], 
        'Doanh nhân': [2,26702], 
        'Gaming': [3,26695], 
        'Học sinh - sinh viên': [5,26699], 
        'Sinh viên văn phòng': [8,26696], 
        'Thiết kế đồ hoạ': [2, 26697]
    }
    
    name = 'LapFeature'
    
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=' + str(features['Doanh nghiệp'][1]),
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=' + str(features['Doanh nhân'][1]),
    ]
    
class DoanhnghiepSpider(scrapy.Spider):
    name = 'doanhnghiep'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26698&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = PhongvuItem()
        
        items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['Name'] = item
            
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26698&page=' + str(self.page_number)
        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
            
class DoanhnhanSpider(scrapy.Spider):
    name = 'doanhnhan'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26702&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = PhongvuItem()
        
        items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['Name'] = item
            
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26702&page=' + str(self.page_number)
        if self.page_number <= 2:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
        
class GamingSpider(scrapy.Spider):
    name = 'gaming'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26695&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = PhongvuItem()
        
        items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['Name'] = item
            
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26695&page=' + str(self.page_number)
        if self.page_number <= 3:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
            
class HocsinhsinhvienSpider(scrapy.Spider):
    name = 'hocsinhsinhvien'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26699&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = PhongvuItem()
        
        items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['Name'] = item
            
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26699&page=' + str(self.page_number)
        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
            
class VanphongSpider(scrapy.Spider):
    name = 'vanphong'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26696&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = PhongvuItem()
        
        items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['Name'] = item
            
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26696&page=' + str(self.page_number)
        if self.page_number <= 8:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
            
class ThietkedohoaSpider(scrapy.Spider):
    name = 'thietkedohoa'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26697&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = PhongvuItem()
        
        items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['Name'] = item
            
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26697&page=' + str(self.page_number)
        if self.page_number <= 2:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
'''       
        
        
        
        
                    
            
            
    
        
    
