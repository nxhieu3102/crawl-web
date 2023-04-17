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

class CPSLaptopLinkSpider(scrapy.Spider):
    name = 'CPSLaptopLink'
    start_urls = [
        'https://cellphones.com.vn/laptop.html'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.driver.implicitly_wait(5)
                a_tag = self.driver.find_element(By.CSS_SELECTOR,'#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a')
                self.driver.execute_script("arguments[0].click();", a_tag)
            except:
                break
                        
        for item in self.driver.find_elements(By.CSS_SELECTOR,'.product-info-container .product-info .product__link'):
            instance['ProductLink'] = item.get_attribute('href')
            yield instance
        
class CPSLaptopDetailSpider(scrapy.Spider):
    loaded = ''
    with open('./scraper/links/CPSLaptopLink.json') as value:
        loaded = json.load(value)
        
    name = 'CPSLaptopDetail'
    index = 82
    
    print(len(loaded))
    
    start_urls = [
        loaded[81]['ProductLink']
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 5)
            
    def parse(self, response):
        
        self.driver.get(response.url)
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except:
                 break
        
        instance = ProductItem()
        
        instance['ProductID'] = 'CPSLAP' + str(self.index)
        #layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.box-header.is-flex.is-align-items-center.box-header-desktop > div.box-product-name > h1
        try:
            instance['ProductName'] = self.driver.find_element(By.CSS_SELECTOR,'div.box-product-name > h1').text.strip()
        except NoSuchElementException as e:
            instance['ProductName'] = ''
        
        
        #breadcrumbs > div.block-breadcrumbs.affix > div > ul > li:nth-child(3) > a
        try:
            instance['BrandName'] = self.driver.find_element(By.CSS_SELECTOR,'#breadcrumbs > div.block-breadcrumbs.affix > div > ul > li:nth-child(3) > a').text.upper()
            if instance['BrandName'] == 'MAC':
                instance['BrandName'] = 'APPLE'
        except NoSuchElementException as e:
            instance['BrandName'] = ''
            
        instance['ShopName'] = 'CellPhoneS'
        
        try:
            instance['ImageLink'] = self.driver.find_element(By.XPATH,'//*[@id="layout-desktop"]/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/img').get_attribute('src')
        except NoSuchElementException as e:
            instance['ImageLink'] = ''
        
        instance['ProductLink'] = self.loaded[self.index - 1]['ProductLink']
        
        try:
            instance['SalePrice'] = self.driver.find_element(By.CSS_SELECTOR,'.product__price--show').text
        except NoSuchElementException as e:
            instance['SalePrice'] = ''
        
        try:
            instance['NormalPrice'] = self.driver.find_element(By.CSS_SELECTOR,'.product__price--through').text
        except NoSuchElementException as e:
            instance['NormalPrice'] = instance['SalePrice']
            
        instance['Type'] = 'Máy tính cá nhân'
        
        mapping = {
            "Loại card đồ họa": "Đồ họa",
            "Dung lượng RAM": "RAM",
            "Ổ cứng": "Lưu trữ",
            "Công nghệ màn hình": "Màn hình",
            "Pin": "Pin",
            "Hệ điều hành": "Hệ điều hành",
        }
        
        instance['ConfigDetail'] = {}
        
        selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.block-content-product > div.block-content-product-right > div > ul > li:nth-child({})'
        for i in range(1,11):
            try:
                pattern = self.driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > p').text
                detail = self.driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > div').text
                for key in mapping.keys():
                    if pattern == key:
                        instance['ConfigDetail'][mapping[pattern]] = detail
                        break
            except NoSuchElementException as e:
                pass
        
        instance['PromotionDetail'] = []
        selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.box-detail-product.columns.m-0 > div.box-detail-product__box-center.column.is-one-third > div:nth-child(4) > div > div.box-product-promotion-content.px-2.pt-2.show-all > div:nth-child({}) > a'
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
        
class CPSLaptopGamingSpider(scrapy.Spider):
    name = 'CPSLaptopGaming'
    start_urls = [
        'https://phongvu.vn/c/laptop?attributes.nhucausudung=26695&page=1'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.driver.implicitly_wait(5)
                a_tag = self.driver.find_element(By.CSS_SELECTOR,'#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a')
                self.driver.execute_script("arguments[0].click();", a_tag)
            except:
                break
                        
        for item in self.driver.find_elements(By.CSS_SELECTOR,'.product-info-container .product-info .product__link'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['ProductLink'] = item.get_attribute('href')
            instance['FeatureDetail'] = 'Gaming'

            yield instance
            
class CPSLaptopHocsinhsinhvienSpider(scrapy.Spider):
    name = 'CPSLaptopHocsinhsinhvien'
    start_urls = [
        'https://cellphones.com.vn/laptop/sinh-vien.html'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.driver.implicitly_wait(5)
                a_tag = self.driver.find_element(By.CSS_SELECTOR,'#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a')
                self.driver.execute_script("arguments[0].click();", a_tag)
            except:
                break
                        
        for item in self.driver.find_elements(By.CSS_SELECTOR,'.product-info-container .product-info .product__link'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['ProductLink'] = item.get_attribute('href')
            instance['FeatureDetail'] = 'Học sinh - Sinh viên'

            yield instance
    
class CPSLaptopVanphongSpider(scrapy.Spider):
    name = 'CPSLaptopVanphong'
    start_urls = [
        'https://cellphones.com.vn/laptop/van-phong.html'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.driver.implicitly_wait(5)
                a_tag = self.driver.find_element(By.CSS_SELECTOR,'#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a')
                self.driver.execute_script("arguments[0].click();", a_tag)
            except:
                break
                        
        for item in self.driver.find_elements(By.CSS_SELECTOR,'.product-info-container .product-info .product__link'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['ProductLink'] = item.get_attribute('href')
            instance['FeatureDetail'] = 'Văn phòng'

            yield instance
    
class CPSLaptopThietkedohoaSpider(scrapy.Spider):
    name = 'CPSLaptopThietkedohoa'
    start_urls = [
        'https://cellphones.com.vn/laptop/do-hoa.html'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.driver.implicitly_wait(5)
                a_tag = self.driver.find_element(By.CSS_SELECTOR,'#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a')
                self.driver.execute_script("arguments[0].click();", a_tag)
            except:
                break
                        
        for item in self.driver.find_elements(By.CSS_SELECTOR,'.product-info-container .product-info .product__link'):
            instance['ProductID'] = None
            instance['ProductName'] = ''
            instance['BrandName'] = ''
            instance['ShopName'] = ''
            instance['ImageLink'] = ''
            instance['SalePrice'] = ''
            instance['NormalPrice']= ''
            instance['Type'] = ''
            instance['ProductLink'] = item.get_attribute('href')
            instance['FeatureDetail'] = 'Thiết kế đồ hoạ'

            yield instance
            
class CPSPhoneLinkSpider(scrapy.Spider):
    name = 'CPSPhoneLink'
    start_urls = [
        'https://cellphones.com.vn/mobile.html'
    ]
    
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 5)
    
    def parse(self, response):
        instance = ProductItem()
        
        self.driver.get(response.url)
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.driver.implicitly_wait(10)
                a_tag = self.driver.find_element(By.CSS_SELECTOR,'#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a')
                self.driver.execute_script("arguments[0].click();", a_tag)
            except:
                break
                        
        for item in self.driver.find_elements(By.CSS_SELECTOR,'.product-info-container .product-info .product__link'):
            instance['ProductLink'] = item.get_attribute('href')
            yield instance
         
class CPSPhoneDetailSpider(scrapy.Spider):
    loaded = ''
    with open('./scraper/links/CPSPhoneLink.json') as value:
        loaded = json.load(value)
        
    name = 'CPSPhoneDetail'
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

        instance['ProductID'] = 'CPSPHONE' + str(self.index)
        
        try:
            instance['ProductName'] = self.driver.find_element(By.CSS_SELECTOR,'div.box-product-name > h1').text.strip()
        except NoSuchElementException as e:
            instance['ProductName'] = ''
            
        try:
            instance['BrandName'] = self.driver.find_element(By.CSS_SELECTOR,'#breadcrumbs > div.block-breadcrumbs.affix > div > ul > li:nth-child(3) > a').text.upper()
        except NoSuchElementException as e:
            instance['BrandName'] = ''
            
        instance['ShopName'] = 'CellPhoneS'
        
        try:
            instance['ImageLink'] = self.driver.find_element(By.XPATH,'//*[@id="layout-desktop"]/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/img').get_attribute('src')
        except NoSuchElementException as e:
            instance['ImageLink'] = ''
        
        instance['ProductLink'] = self.loaded[self.index - 1]['ProductLink']
        
        try:
            instance['SalePrice'] = self.driver.find_element(By.CSS_SELECTOR,'.product__price--show').text
        except NoSuchElementException as e:
            instance['SalePrice'] = ''
        
        try:
            instance['NormalPrice'] = self.driver.find_element(By.CSS_SELECTOR,'.product__price--through').text
        except NoSuchElementException as e:
            instance['NormalPrice'] = instance['SalePrice']
            
        instance['Type'] = 'Điện thoại'

        mapping = {
            "Công nghệ màn hình": "Màn hình",
            "Camera sau": "Camera sau",
            "Camera trước": "Camera Selfie",
            "Chipset": "CPU",
            "Dung lượng RAM": "RAM",
            "Bộ nhớ trong": "Bộ nhớ trong",
            "Pin": "Pin",
            "Thẻ SIM": "Thẻ sim",
            "Hệ điều hành": "Hệ điều hành"
        }
        
        instance['ConfigDetail'] = {}
        
        selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.block-content-product > div.block-content-product-right > div > ul > li:nth-child({})'
        for i in range(1,11):
            try:
                pattern = self.driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > p').text
                detail = self.driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > div').text
                for key in mapping.keys():
                    if pattern == key:
                        instance['ConfigDetail'][mapping[pattern]] = detail
                        break
            except NoSuchElementException as e:
                pass
        
        instance['PromotionDetail'] = []
        selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.box-detail-product.columns.m-0 > div.box-detail-product__box-center.column.is-one-third > div:nth-child(4) > div > div.box-product-promotion-content.px-2.pt-2.show-all > div:nth-child({}) > a'
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

