import scrapy
from ..items import ProductItem
import json

class PVLaptopLinkSpider(scrapy.Spider):
    name = 'PVLaptopLink'
    page_number = 2
    start_urls = [
        'https://phongvu.vn/c/laptop?page=1'
    ]
    
    def parse(self, response):
        
        instance = ProductItem()
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()
    
        for item in items:
            instance['ProductID'] = '', 
            instance['ProductName'] = '', 
            instance['BrandName'] = '', 
            instance['ShopName'] = '', 
            instance['ImageLink'] = '', 
            instance['SalePrice'] = '', 
            instance['NormalPrice']= '', 
            instance['Type'] = '',
            instance['ProductLink'] = 'https://phongvu.vn' + item
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?page=' + str(self.page_number)
        if self.page_number <= 1:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
 
class PVLaptopDetailSpider(scrapy.Spider):
    loaded = ''
    with open('./scraper/links/PVLaptopLink.json') as value:
        loaded = json.load(value)
        
    name = 'PVLaptopDetail'
    index = 1
    
    start_urls = [
        loaded[0]['ProductLink']
    ]
            
    def parse(self, response):
        
        instance = ProductItem()
        
        instance['ProductID'] = 'PVLAP' + str(self.index)
        instance['ProductName'] = response.css('.css-4kh4rf::text').extract()[0]
        
        instance['BrandName'] = response.css('.css-n67qkj::text').extract()[0]
        instance['ShopName'] = 'PhongVu'
        
        instance['ImageLink'] = response.css('.css-j4683g img::attr(src)').extract()[0]
        instance['ProductLink'] = self.loaded[self.index - 1]['ProductLink']

        instance['SalePrice'] = response.css('.css-1q5zfcu .att-product-detail-latest-price::text').extract()[0]
        
        temp = response.css('.css-1q5zfcu .att-product-detail-retail-price::text').extract()
        if len(temp) == 0:
            instance['NormalPrice'] = instance['SalePrice']
        else: instance['NormalPrice'] = temp[0]
       
        instance['ConfigDetail'] = response.css('.css-17aam1::text').extract()
        if len(instance['ConfigDetail']) == 0:
            instance['ConfigDetail'] = response.css('.css-17aam1 p::text').extract()
            
        instance['Type'] = 'Máy tính cá nhân'
        
        temp = response.css('.css-hr6z5n::text').extract()
        if len(temp) == 0:
            instance['PromotionDetail'] = ''
        else: instance['PromotionDetail'] = temp
        
        instance['FeatureDetail'] = []
        
        yield instance
        
        if self.index < len(self.loaded):
            next_page = self.loaded[self.index]['ProductLink']
        else: next_page = ''
        
        if self.index <= len(self.loaded) - 1:
            self.index += 1
            yield response.follow(next_page, callback = self.parse)

class PVLaptopDoanhnghiepSpider(scrapy.Spider):
    name = 'PVLaptopDoanhnghiep'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26698&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()

        for item in items:
            instance['ProductLink'] = item
            instance['FeatureDetail'] = 'Doanh nghiệp'
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26698&page=' + str(self.page_number)
        if self.page_number <= 1:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
            
class PVLaptopDoanhnhanSpider(scrapy.Spider):
    name = 'PVLaptopDoanhnhan'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26702&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()
                
        for item in items:
            instance['ProductLink'] = item
            instance['FeatureDetail'] = 'Doanh nhân'
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26702&page=' + str(self.page_number)
        if self.page_number <= 2:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
        
class PVLaptopGamingSpider(scrapy.Spider):
    name = 'PVLaptopGaming'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26695&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()
                
        for item in items:
            instance['ProductLink'] = item
            instance['FeatureDetail'] = 'Doanh nhân'
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26695&page=' + str(self.page_number)
        if self.page_number <= 3:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
            
class PVLaptopHocsinhsinhvienSpider(scrapy.Spider):
    name = 'PVLaptopHocsinhsinhvien'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26699&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['Name'] = item
            
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26699&page=' + str(self.page_number)
        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
            
class PVLaptopVanphongSpider(scrapy.Spider):
    name = 'PVLaptopVanphong'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26696&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['Name'] = item
            
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26696&page=' + str(self.page_number)
        if self.page_number <= 8:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
            
class PVLaptopThietkedohoaSpider(scrapy.Spider):
    name = 'PVLaptopThietkedohoa'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26697&page=1'
    ]
    page_number = 2
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['Name'] = item
            
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26697&page=' + str(self.page_number)
        if self.page_number <= 2:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)

        
        
        
        
                    
            
            
    
        
    
