import scrapy
from ..items import ProductItem
import json
from random import choice
from ..LinkProcess import csvToList, addLinkToCSV

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

class PVLaptopLinkSpider(scrapy.Spider):
    name = 'PVLaptopLink'
    page_number = 2
    start_urls = [
        'https://phongvu.vn/c/laptop?page=1'
    ]
    
    def parse(self, response):
        loaded = csvToList('./scraper/links/pv/laptop.csv')
        
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()
    
        for item in items:
            link = 'https://phongvu.vn' + item
            flag = True
            for i in loaded:
                if i[0] == link:
                    flag = False
                    break
            if flag:
                addLinkToCSV('./scraper/links/pv/laptop.csv',[link])
            
        next_page = 'https://phongvu.vn/c/laptop?page=' + str(self.page_number)
        if self.page_number <= 25:
            self.page_number += 1
            yield response.follow(url = next_page, callback = self.parse, headers = choice(CUSTOM_HEADERS))
 
class PVLaptopDetailSpider(scrapy.Spider):
    loaded = csvToList('./scraper/links/pv/laptop.csv')

        
    name = 'PVLaptopDetail'
    index = 1
    
    start_urls = [
        loaded[0][0]
    ]
            
    def parse(self, response):
        
        instance = ProductItem()
        
        instance['ProductID'] = 'PVLAP' + str(self.index)
        
        tmp = response.css('.css-4kh4rf::text').extract()
        if len(tmp):
            instance['ProductName'] = tmp[0]
        else: instance['ProductName'] = ''
        
        tmp = response.css('.css-n67qkj::text').extract()
        if len(tmp):
            instance['BrandName'] = tmp[0]
        else: instance['BrandName'] = ''
        instance['ShopName'] = 'PhongVu'
        
        tmp = response.css('.css-j4683g img::attr(src)').extract()
        if len(tmp):
            instance['ImageLink'] = tmp[0]
        else: instance['ImageLink'] = ''
        
        instance['ProductLink'] = self.loaded[self.index - 1][0]
        
        tmp = response.css('.css-1q5zfcu .att-product-detail-latest-price::text').extract()
        if len(tmp):
            instance['SalePrice'] = tmp[0]
        else: instance['SalePrice'] = ''
        
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
            next_page = self.loaded[self.index][0]
        else: next_page = ''
        
        if self.index <= len(self.loaded) - 1:
            self.index += 1
            yield response.follow(next_page, callback = self.parse, headers = choice(CUSTOM_HEADERS))

class PVLaptopDoanhnghiepSpider(scrapy.Spider):
    name = 'PVLaptopDoanhnghiep'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26698&page=1'
    ]
    page_number = 1
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()

        for item in items:
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['ProductLink'] = 'https://phongvu.vn' + item
            instance['FeatureDetail'] = 'Doanh nhân'
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26698&page=' + str(self.page_number)
        if self.page_number <= 4:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse, headers = choice(CUSTOM_HEADERS))
            
class PVLaptopDoanhnhanSpider(scrapy.Spider):
    name = 'PVLaptopDoanhnhan'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26702&page=1'
    ]
    page_number = 1
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()
                
        for item in items:
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['ProductLink'] = 'https://phongvu.vn' + item
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
    page_number = 1
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()
                
        for item in items:
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['ProductLink'] = 'https://phongvu.vn' + item
            instance['FeatureDetail'] = 'Gaming'
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
    page_number = 1
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()

        #items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['ProductLink'] = 'https://phongvu.vn' + item
            instance['FeatureDetail'] = 'Học sinh - Sinh viên'
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
    page_number = 1
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()

        #items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['ProductLink'] = 'https://phongvu.vn' + item
            instance['FeatureDetail'] = 'Văn phòng'
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
    page_number = 1
    
    
    def parse(self, response):
        
        instance = ProductItem()
        
        items = response.css('.css-13w7uog .css-35xksx .css-pxdb0j::attr(href)').extract()

        #items = response.css('.css-1xdyrhj::text').extract()
        
        for item in items:
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['ProductLink'] = 'https://phongvu.vn' + item
            instance['FeatureDetail'] = 'Thiết kế đồ hoạ'
            yield instance
            
        next_page = 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26697&page=' + str(self.page_number)
        if self.page_number <= 2:
            self.page_number += 1
            yield response.follow(next_page, callback = self.parse)
            

