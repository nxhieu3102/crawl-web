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
from ..LinkProcess import csvToList, addLinkToCSV


options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu");

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
    '''
    with open('./scraper/links/cps/laptop.csv') as value:
        loaded = json.load(value)
    '''
    file = open('./scraper/links/cps/laptop.csv')
    csvreader = csv.reader(file)

    loaded = []
    for row in csvreader:
        loaded.append(row)
        
    name = 'CPSLaptopDetail'
    index = 1
    
    
    start_urls = [
        #loaded[60]['ProductLink']
        loaded[0][0]
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
        except NoSuchElementException:
            instance['ProductName'] = ''
        
        
        #breadcrumbs > div.block-breadcrumbs.affix > div > ul > li:nth-child(3) > a
        try:
            instance['BrandName'] = self.driver.find_element(By.CSS_SELECTOR,'#breadcrumbs > div.block-breadcrumbs.affix > div > ul > li:nth-child(3) > a').text.upper()
            if instance['BrandName'] == 'MAC':
                instance['BrandName'] = 'APPLE'
        except NoSuchElementException:
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
            
        instance['ShopName'] = 'CellPhoneS'
        
        try:
            instance['ImageLink'] = self.driver.find_element(By.XPATH,'//*[@id="layout-desktop"]/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/img').get_attribute('src')
        except NoSuchElementException:
            instance['ImageLink'] = ''
        
        instance['ProductLink'] = self.loaded[self.index - 1][0]#self.loaded[self.index - 1]['ProductLink']
        
        print(instance['ProductLink'])
        
        try:
            instance['SalePrice'] = self.driver.find_element(By.CSS_SELECTOR,'.product__price--show').text
        except NoSuchElementException:
            instance['SalePrice'] = ''
        
        try:
            instance['NormalPrice'] = self.driver.find_element(By.CSS_SELECTOR,'.product__price--through').text
        except NoSuchElementException:
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
                #for key in mapping.keys():
                    #if pattern == key:
                if pattern in mapping:
                    instance['ConfigDetail'][mapping[pattern]] = detail
                else: instance['ConfigDetail'][pattern] = detail
            except NoSuchElementException:
                pass
        
        instance['PromotionDetail'] = []
        selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.box-detail-product.columns.m-0 > div.box-detail-product__box-center.column.is-one-third > div:nth-child(4) > div > div.box-product-promotion-content.px-2.pt-2.show-all > div:nth-child({}) > a'
        for i in range(1,4):
            try:
                detail = self.driver.find_element(By.CSS_SELECTOR, selector.format(i)).text
                instance['PromotionDetail'].append(detail)
            except NoSuchElementException:
                pass 
            
        instance['FeatureDetail'] = []
            
        yield instance
        
        #print(instance)
        
        if self.index < len(self.loaded):
            next_page = self.loaded[self.index][0]#['ProductLink']
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
    file = open('./scraper/links/cps/phone.csv')
    csvreader = csv.reader(file)
    
    loaded = []
    for row in csvreader:
        loaded.append(row)
        
    name = 'CPSPhoneDetail'
    index = 1
    
    
    start_urls = [
        loaded[0][0]
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
        except NoSuchElementException:
            instance['ProductName'] = ''
            
        try:
            instance['BrandName'] = self.driver.find_element(By.CSS_SELECTOR,'#breadcrumbs > div.block-breadcrumbs.affix > div > ul > li:nth-child(3) > a').text.upper()
        except NoSuchElementException:
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
            
        instance['ShopName'] = 'CellPhoneS'
        
        try:
            instance['ImageLink'] = self.driver.find_element(By.XPATH,'//*[@id="layout-desktop"]/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/img').get_attribute('src')
        except NoSuchElementException:
            instance['ImageLink'] = ''
        
        instance['ProductLink'] = self.loaded[self.index - 1][0]
        
        try:
            instance['SalePrice'] = self.driver.find_element(By.CSS_SELECTOR,'.product__price--show').text
        except NoSuchElementException:
            instance['SalePrice'] = ''
        
        try:
            instance['NormalPrice'] = self.driver.find_element(By.CSS_SELECTOR,'.product__price--through').text
        except NoSuchElementException:
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
                if pattern in mapping:
                    instance['ConfigDetail'][mapping[pattern]] = detail
                else: instance['ConfigDetail'][pattern] = detail
            except NoSuchElementException:
                pass
        
        instance['PromotionDetail'] = []
        selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.box-detail-product.columns.m-0 > div.box-detail-product__box-center.column.is-one-third > div:nth-child(4) > div > div.box-product-promotion-content.px-2.pt-2.show-all > div:nth-child({}) > a'
        for i in range(1,4):
            try:
                detail = self.driver.find_element(By.CSS_SELECTOR, selector.format(i)).text
                instance['PromotionDetail'].append(detail)
            except NoSuchElementException:
                pass 
            
        instance['FeatureDetail'] = []
            
        yield instance
        
        if self.index < len(self.loaded):
            next_page = self.loaded[self.index][0]
        else: next_page = ''
        
        if self.index <= len(self.loaded) - 1:
            self.index += 1
            yield response.follow(next_page, callback = self.parse)



# class CPSLaptopLinkSpider(scrapy.Spider):
#     name = 'CPSLaptopLink'
#     start_urls = [
#         'https://cellphones.com.vn/laptop.html'
#     ]

#     def __init__(self):
#         self.driver = webdriver.Chrome(chrome_options=options)
#         self.wait = WebDriverWait(self.driver, 10)
    
#     def parse(self, response):
#         loaded = csvToList('./scraper/links/cps/laptop.csv')
#         self.driver.get(response.url)
#         while True:
#             self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             try:
#                 self.driver.implicitly_wait(5)
#                 a_tag = self.driver.find_element(By.CSS_SELECTOR,'#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a')
#                 self.driver.execute_script("arguments[0].click();", a_tag)
#             except:
#                 break
                        
#         for item in self.driver.find_elements(By.CSS_SELECTOR,'.product-info-container .product-info .product__link'):
#             link = item.get_attribute('href')
#             flag = True
#             for i in self.loaded:
#                 if i[0] == link:
#                     flag = False
#                     break
#             if flag:
#                 addLinkToCSV('./scraper/links/cps/laptop.csv',[link])