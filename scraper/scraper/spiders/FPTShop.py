# -*- coding: utf-8 -*- 
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
options.add_argument("--disable-gpu");


class FPTLaptopLinkSpider(scrapy.Spider):
    name = 'FPTLaptopLink'
    start_urls = [
        'https://fptshop.com.vn/may-tinh-xach-tay?sort=ban-chay-nhat&trang=9'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except:
                 break

        for item in self.driver.find_elements(By.CSS_SELECTOR,'.cdt-product__info .cdt-product__name'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = ''
            instance['ProductLink'] = item.get_attribute('href')
            yield instance
        
        
class FPTLaptopDetailSpider(scrapy.Spider):
    loaded = ''
    with open('./scraper/links/fpt/laptop.json') as value:
        loaded = json.load(value)
        
    name = 'FPTLaptopDetail'
    index = 1
    
    start_urls = [
        loaded[0]['ProductLink']
    ]
        
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 5)
            
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except:
                 break

        instance['ProductID'] = 'FPTLAP' + str(self.index)
        
        try:
            instance['ProductName'] = self.driver.find_element(By.CSS_SELECTOR, '.st-name').text
            pattern = r'\(.*?\)'
            instance['ProductName'] = re.sub(pattern,'',instance['ProductName'])
        except NoSuchElementException:
            instance['ProductName'] = ''
        #root > main > div > div.l-pd-header > div:nth-child(1) > div > ol > li.breadcrumb-item.active > a
        try:
            instance['BrandName'] = self.driver.find_element(By.CSS_SELECTOR, 'li.breadcrumb-item.active > a').text
            instance['BrandName'] = instance['BrandName'].upper()
        except NoSuchElementException:
            if instance['ProductName']:
                brands = ['macbook' , 'asus' , 'hp' , 'lenovo' , 'acer' , 'dell' ,
                    'msi' , 'surface' , 'itel' , 'masstel' , 'chuwi' , 'lg', 'gigabyte']
                for brand in brands:
                    if brand.upper() in instance['ProductName'].upper():
                        if brand == 'macbook':
                            brand = 'APPLE'
                        instance['BrandName'] = brand.upper()
                        break
            else: instance['BrandName'] = ''
                
        instance['ShopName'] = 'FPTShop'
        
        try:
            instance['ImageLink'] = self.driver.find_element(By.CSS_SELECTOR, 'div.swiper-slide.swiper-slide-active > img').get_attribute('src')
        except NoSuchElementException:
            instance['ImageLink'] = ''
        
        instance['ProductLink'] = self.loaded[self.index - 1]['ProductLink']

        print(instance['ProductLink'])
        #root > main > div > div.l-pd-header.selectorgadget_selected > div:nth-child(2) > div.l-pd-row.clearfix > div.l-pd-right > div.st-price > div > div.st-price-main
        try:
            instance['SalePrice'] = self.driver.find_element(By.CSS_SELECTOR, 'div.st-price > div > div.st-price-main').text
        except NoSuchElementException:
            instance['SalePrice'] = ''
        try:
            instance['NormalPrice'] = self.driver.find_element(By.CSS_SELECTOR, 'div.st-price > div > div.st-price-sub > strike').text
        except NoSuchElementException:
            instance['NormalPrice'] = instance['SalePrice']

        mapping = {
            "Màn hình": "Màn hình",
            "CPU": "CPU",
            "RAM": "RAM",
            "Ổ cứng": "Lưu trữ",
            "Đồ họa": "Đồ họa",
            "Hệ điều hành": "Hệ điều hành",
            "Trọng lượng": "Khối lượng",
            "Kích thước": "Kích thước"
        }
        #ConfigPattern = ["Màn hình", "CPU", "RAM", "Lưu trữ", "Đồ hoạ", "Hệ điều hành", "Khối lượng"]
        instance['ConfigDetail'] = {}
        selector = '#root > main > div > div.l-pd-body > div > div.l-pd-body__wrapper > div.l-pd-body__right > div.card.re-card.st-card > div > table > tbody > tr:nth-child({})'
        for i in range(1,8):
            try:
                pattern = self.driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > td:nth-child(1)').text
                detail = self.driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > td:nth-child(2)').text
                if pattern in mapping:
                    instance['ConfigDetail'][mapping[pattern]] = detail
            except NoSuchElementException as e:
                pass
                
        instance['Type'] = 'Máy tính cá nhân'
        
        selector = '#root > main > div > div.l-pd-header > div:nth-child(2) > div.l-pd-row.clearfix > div.l-pd-right > div.st-boxPromo > ul > li:nth-child({}) > div > span'
        instance['PromotionDetail'] = []
        for i in range(1,4):
            try:
                detail = self.driver.find_element(By.CSS_SELECTOR, selector.format(i)).text
                instance['PromotionDetail'].append(detail)
            except NoSuchElementException as e:
                pass 
        
        instance['FeatureDetail'] = []
        
        #print(instance)
        
        yield instance
        
        if self.index < len(self.loaded):
            next_page = self.loaded[self.index]['ProductLink']
        else: next_page = ''
        
        if self.index <= len(self.loaded) - 1:
            self.index += 1
            yield response.follow(next_page, callback = self.parse)
  
          
class FPTLaptopDoanhnhanSpider(scrapy.Spider):
    name = 'FPTLaptopDoanhnhan'
    start_urls = [
        'https://fptshop.com.vn/may-tinh-xach-tay/doanh-nhan?sort=ban-chay-nhat&trang=3'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except:
                 break

        for item in self.driver.find_elements(By.CSS_SELECTOR,'.cdt-product__info .cdt-product__name'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = 'Doanh nhân'
            instance['ProductLink'] = item.get_attribute('href')
            yield instance
        
class FPTLaptopGamingSpider(scrapy.Spider):
    name = 'FPTLaptopGaming'
    start_urls = [
        'https://fptshop.com.vn/may-tinh-xach-tay/gaming-do-hoa?sort=ban-chay-nhat&trang=2'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except:
                 break

        for item in self.driver.find_elements(By.CSS_SELECTOR,'.cdt-product__info .cdt-product__name'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = 'Gaming'
            instance['ProductLink'] = item.get_attribute('href')
            yield instance
    
class FPTLaptopHocsinhsinhvienSpider(scrapy.Spider):
    name = 'FPTLaptopHocsinhsinhvien'
    start_urls = [
        'https://fptshop.com.vn/may-tinh-xach-tay/sinh-vien-van-phong?sort=ban-chay-nhat&trang=5'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except:
                 break

        for item in self.driver.find_elements(By.CSS_SELECTOR,'.cdt-product__info .cdt-product__name'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = 'Học sinh - Sinh viên'
            instance['ProductLink'] = item.get_attribute('href')
            yield instance
            
class PVLaptopThietkedohoaSpider(scrapy.Spider):
    name = 'FPTLaptopThietkedohoa'
    start_urls = [
        'https://fptshop.com.vn/may-tinh-xach-tay/thiet-ke?sort=ban-chay-nhat&trang=2'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except:
                 break

        for item in self.driver.find_elements(By.CSS_SELECTOR,'.cdt-product__info .cdt-product__name'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = 'Thiết kế đồ hoạ'
            instance['ProductLink'] = item.get_attribute('href')
            yield instance
            

class FPTPhoneLinkSpider(scrapy.Spider):
    name = 'FPTPhoneLink'
    start_urls = [
        'https://fptshop.com.vn/dien-thoai?sort=ban-chay-nhat&trang=4'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except:
                 break

        for item in self.driver.find_elements(By.CSS_SELECTOR,'.cdt-product__info .cdt-product__name'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = ''
            instance['ProductLink'] = item.get_attribute('href')
            yield instance
        
        
class FPTPhoneDetailSpider(scrapy.Spider):
    loaded = ''
    with open('./scraper/links/fpt/phone.json') as value:
        loaded = json.load(value)
        
    name = 'FPTPhoneDetail'
    index = 81
    
    start_urls = [
        loaded[80]['ProductLink']
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 5)
            
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except:
                 break

        instance['ProductID'] = 'FPTPHONE' + str(self.index)
        try:
            instance['ProductName'] = self.driver.find_element(By.CSS_SELECTOR, '.st-name').text
            pattern = r'\(.*?\)'
            instance['ProductName'] = re.sub(pattern,'',instance['ProductName'])
        except NoSuchElementException:
            instance['ProductName'] = ''
        #root > main > div > div.l-pd-header > div:nth-child(1) > div > ol > li.breadcrumb-item.active > a
        try:
            instance['BrandName'] = self.driver.find_element(By.CSS_SELECTOR, 'li.breadcrumb-item.active > a').text.upper()
        except NoSuchElementException:
            if instance['ProductName']:
                brands = ['iphone' , 'samsung' , 'oppo' , 'xiaomi' , 'vivo' , 'realme' , 
                  'nokia' , 'tcl' , 'mobell' , 'itel' , 'masstel']
                for brand in brands:
                    if brand.upper() in instance['ProductName'].upper():
                        if brand == 'iphone':
                            brand = 'APPLE'
                        instance['BrandName'] = brand.upper()
                        break
            else: instance['BrandName'] = ''
                
                
        instance['ShopName'] = 'FPTShop'
        
        try:
            instance['ImageLink'] = self.driver.find_element(By.CSS_SELECTOR, 'div.swiper-slide.swiper-slide-active > img').get_attribute('src')
        except NoSuchElementException:
            instance['ImageLink'] = ''
        
        instance['ProductLink'] = self.loaded[self.index - 1]['ProductLink']

        
        #root > main > div > div.l-pd-header.selectorgadget_selected > div:nth-child(2) > div.l-pd-row.clearfix > div.l-pd-right > div.st-price > div > div.st-price-main
        try:
            instance['SalePrice'] = self.driver.find_element(By.CSS_SELECTOR, 'div.st-price > div > div.st-price-main').text
        except NoSuchElementException as e:
            instance['SalePrice'] = ''
        try:
            instance['NormalPrice'] = self.driver.find_element(By.CSS_SELECTOR, 'div.st-price > div > div.st-price-sub > strike').text
        except NoSuchElementException as e:
            instance['NormalPrice'] = instance['SalePrice']
       
        mapping = {
            "Bộ nhớ trong": "Lưu trữ",
            "Màn hình": "Màn hình",
            "Hệ điều hành": "Hệ điều hành",
            "Pin": "Pin",
            "Camera sau": "Camera sau",
            "Camera Selfie": "Camera trước"
        }
        #ConfigPattern = ["Màn hình", "Camera sau", "Camera Selfie", "RAM", "Bộ nhớ trong", "CPU", "Pin","Thẻ sim","Hệ điều hành"]
        instance['ConfigDetail'] = {}
        #root > main > div > div.l-pd-body > div > div.l-pd-body__wrapper > div.l-pd-body__right > div:nth-child(1) > div > table > tbody > tr:nth-child(1) > td:nth-child(1)
        #root > main > div > div.l-pd-body > div > div.l-pd-body__wrapper > div.l-pd-body__right > div:nth-child(1) > div > table > tbody > tr:nth-child(2) > td:nth-child(1)
        selector = '#root > main > div > div.l-pd-body > div > div.l-pd-body__wrapper > div.l-pd-body__right > div:nth-child(1) > div > table > tbody > tr:nth-child({})'
        for i in range(1,10):
            try:
                pattern = self.driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > td:nth-child(1)').text
                detail = self.driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > td:nth-child(2)').text
                if pattern in mapping:
                    instance['ConfigDetail'][mapping[pattern]] = detail
                else: instance['ConfigDetail'][pattern] = detail
            except NoSuchElementException:
                pass
                
        instance['Type'] = 'Điện thoại'
        
        selector = '#root > main > div > div.l-pd-header > div:nth-child(2) > div.l-pd-row.clearfix > div.l-pd-right > div.st-boxPromo > ul > li:nth-child({}) > div > span'
        instance['PromotionDetail'] = []
        for i in range(1,4):
            try:
                detail = self.driver.find_element(By.CSS_SELECTOR, selector.format(i)).text
                instance['PromotionDetail'].append(detail)
            except NoSuchElementException as e:
                pass 
        
        instance['FeatureDetail'] = []
        
        yield instance
        
        if self.index < len(self.loaded):
            next_page = self.loaded[self.index]['ProductLink']
        else: next_page = ''
        
        if self.index <= len(self.loaded) - 1:
            self.index += 1
            yield response.follow(next_page, callback = self.parse)
            
class FPTPhoneBaomatvantaySpider(scrapy.Spider):
    name = 'FPTPhoneBaomatvantay'
    start_urls = [
        'https://fptshop.com.vn/dien-thoai/bao-mat-van-tay?sort=ban-chay-nhat&trang=2'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except:
                 break

        for item in self.driver.find_elements(By.CSS_SELECTOR,'.cdt-product__info .cdt-product__name'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = 'Bảo mật vân tay'
            instance['ProductLink'] = item.get_attribute('href')
            yield instance
            
class FPTPhoneNhandienkhuonmatSpider(scrapy.Spider):
    name = 'FPTPhoneNhandienkhuonmat'
    start_urls = [
        'https://fptshop.com.vn/dien-thoai/nhan-dien-khuon-mat?sort=ban-chay-nhat&trang=3'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except:
                 break

        for item in self.driver.find_elements(By.CSS_SELECTOR,'.cdt-product__info .cdt-product__name'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['FeatureDetail'] = 'Nhận diện khuôn mặt'
            instance['ProductLink'] = item.get_attribute('href')
            yield instance
