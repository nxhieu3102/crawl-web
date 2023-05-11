from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options

from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product

import csv
from time import sleep
import re

from store.crawl.pipelines import process_item 

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# @shared_task()
# def solve():
def addLinkToCSV(fileLink, productLink):
    with open(fileLink,'a') as fd:
        writer = csv.writer(fd)
        writer.writerow(productLink)
        
def csvToList(fileLink):
    file = open(fileLink)
    csvreader = csv.reader(file)
    header = next(csvreader)  
    rows = []
    for row in csvreader:
        rows.append(row)
    return rows
    
def CellPhoneSUpdateProduct():
    sleep(5)
    loaded = csvToList('./store/links/test2.csv')
    for item in loaded:
        #start_urls = 'https://fptshop.com.vn/may-tinh-xach-tay/asus-tuf-gaming-fx506lhb-hn188w-i5-10300h'
        driver = webdriver.Chrome(chrome_options=options)
        wait = WebDriverWait(driver, 10)
        #print(item[0])
        try:
            driver.get(item[0])
        except WebDriverException:
            break
        
        check_height = driver.execute_script("return document.body.scrollHeight;")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                wait.until(lambda driver: driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = driver.execute_script("return document.body.scrollHeight;") 
            except:
                    break
        
        salePrice = ''
        try:
            salePrice = driver.find_element(By.CSS_SELECTOR,'.product__price--show').text
        except NoSuchElementException:
            pass
        
        normalPrice = ''
        try:
            normalPrice = driver.find_element(By.CSS_SELECTOR,'.product__price--through').text
        except NoSuchElementException:
            pass
        
        if normalPrice != '' and salePrice == '':
            salePrice = normalPrice
        elif normalPrice == '' and salePrice != '':
            normalPrice = salePrice

        #print(salePrice, normalPrice)
        try:
            product = Product.objects.get(ProductLink = item[0])
            if salePrice != '' and normalPrice != '':
                product.SalePrice = salePrice
                product.NormalPrice = normalPrice
                addLinkToCSV('./laptop.csv',["updated cps"])
                product.save()
        except ObjectDoesNotExist:
            pass
            
        driver.close()
    
# def CellPhoneSUpdateLink():
#     sleep(5)
#     start_urls = [
#         ['https://cellphones.com.vn/laptop.html','laptop']
#         ['https://cellphones.com.vn/mobile.html','dienthoai']
#     ]
    
#     for item in start_urls:
                  
#         driver = webdriver.Chrome(chrome_options=options)
#         wait = WebDriverWait(driver, 10)
        
#         try:
#             driver.get(item[0])
#         except WebDriverException:
#             break
        
#         while True:
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             try:
#                 driver.implicitly_wait(10)
#                 a_tag = driver.find_element(By.CSS_SELECTOR,'#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a')
#                 driver.execute_script("arguments[0].click();", a_tag)
#             except:
#                 break
                
#         try:
#             tmp = driver.find_elements(By.CSS_SELECTOR,'.product-info-container .product-info .product__link')
#         except NoSuchElementException:
#             pass
        
#         path = './store/links/test2.csv'
#         loaded = csvToList(path)
#         for item in tmp:
#             link = item.get_attribute('href')
#             flag = True
#             for i in loaded:
#                 if i[0] == link:
#                     flag = False
#                     break
#             if flag:
#                 addLinkToCSV(path,[link, False, item[1]])
        
#         driver.close()
    
    
# def FPTShopUpdateProduct():
#     sleep(5)
#     loaded = csvToList('./store/links/test2.csv')
#     idx = 1
#     for item in loaded:
#         print(item)
#         #start_urls = 'https://fptshop.com.vn/may-tinh-xach-tay/asus-tuf-gaming-fx506lhb-hn188w-i5-10300h'
#         driver = webdriver.Chrome(chrome_options=options)
#         wait = WebDriverWait(driver, 10)
        
#         try:
#             driver.get(item[0])
#         except WebDriverException:
#             break
        
#         check_height = driver.execute_script("return document.body.scrollHeight;")
#         while True:
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             try:
#                 wait.until(lambda driver: driver.execute_script("return document.body.scrollHeight;")  > check_height)
#                 check_height = driver.execute_script("return document.body.scrollHeight;") 
#             except:
#                     break
        
#         if item[1]:
#             salePrice = ''
#             try:
#                 salePrice = driver.find_element(By.CSS_SELECTOR,'.product__price--show').text
#             except NoSuchElementException:
#                 pass
            
#             normalPrice = ''
#             try:
#                 normalPrice = driver.find_element(By.CSS_SELECTOR,'.product__price--through').text
#             except NoSuchElementException:
#                 pass
            
#             if normalPrice != '' and salePrice == '':
#                 salePrice = normalPrice
#             elif normalPrice == '' and salePrice != '':
#                 normalPrice = salePrice

#             print(salePrice,normalPrice)
#             try:
#                 product = Product.objects.get(ProductLink = item[0])
#                 if salePrice != '' and normalPrice != '':
#                     product.SalePrice = salePrice
#                     product.NormalPrice = normalPrice
#                     addLinkToCSV('./laptop.csv',["updated",item,salePrice,normalPrice])
#                     product.save()
#                 else: addLinkToCSV('./laptop.csv',["checked",item,salePrice,normalPrice])
#             except ObjectDoesNotExist:
#                 pass
#         else:
#             productID = ''
#             productName = ''
#             try:
#                 productName = driver.find_element(By.CSS_SELECTOR,'div.box-product-name > h1').text.strip()
#             except NoSuchElementException:
#                 pass
                
#             shopName = 'CellPhoneS'
        
#             imageLink = ''
#             try:
#                 imageLink = driver.find_element(By.XPATH,'//*[@id="layout-desktop"]/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/img').get_attribute('src')
#             except NoSuchElementException:
#                 pass
            
#             productLink = item[0]
            
#             salePrice = ''
#             try:
#                 salePrice = driver.find_element(By.CSS_SELECTOR,'.product__price--show').text
#             except NoSuchElementException:
#                 pass
            
#             normalPrice = ''
#             try:
#                 normalPrice = driver.find_element(By.CSS_SELECTOR,'.product__price--through').text
#             except NoSuchElementException:
#                 pass
            
#             configDetail = {}
#             type = ''
#             brandName = ''
#             if item[2] == 'laptop':
#                 mapping = {
#                     "Loại card đồ họa": "Đồ họa",
#                     "Dung lượng RAM": "RAM",
#                     "Ổ cứng": "Lưu trữ",
#                     "Công nghệ màn hình": "Màn hình",
#                     "Pin": "Pin",
#                     "Hệ điều hành": "Hệ điều hành",
#                 }
                
#                 selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.block-content-product > div.block-content-product-right > div > ul > li:nth-child({})'
#                 for i in range(1,11):
#                     try:
#                         pattern = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > p').text
#                         detail = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > div').text
#                         #for key in mapping.keys():
#                             #if pattern == key:
#                         if pattern in mapping:
#                             configDetail[mapping[pattern]] = detail
#                         else: configDetail[pattern] = detail
#                     except NoSuchElementException:
#                         pass
                    
#                 type = 'Máy tính cá nhân'
                
#                 try:
#                     brandName = driver.find_element(By.CSS_SELECTOR,'#breadcrumbs > div.block-breadcrumbs.affix > div > ul > li:nth-child(3) > a').text.upper()
#                     if brandName == 'MAC':
#                         brandName = 'APPLE'
#                 except NoSuchElementException:
#                     if productName:
#                         brands = ['macbook' , 'asus' , 'hp' , 'lenovo' , 'acer' , 'dell' ,
#                             'msi' , 'surface' , 'itel' , 'masstel' , 'chuwi' , 'lg']
#                         for brand in brands:
#                             if brand.upper() in productName.upper():
#                                 if brand == 'macbook':
#                                     brand = 'APPLE'
#                                 brandName = brand.upper()
#                                 break
                            
#                 productID = 'CPSLAP' + str(idx + 1000)
#             elif item[2] == 'phone':
#                 try:
#                     brandName = driver.find_element(By.CSS_SELECTOR,'#breadcrumbs > div.block-breadcrumbs.affix > div > ul > li:nth-child(3) > a').text.upper()
#                 except NoSuchElementException:
#                     if productName:
#                         brands = ['ipad' , 'samsung' , 'oppo' , 'xiaomi' ,
#                             'nokia' , 'masstel', 'lenovo']
#                         for brand in brands:
#                             if brand.upper() in productName.upper():
#                                 if brand == 'ipad':
#                                     brand = 'APPLE'
#                                 brandName = brand.upper()
#                                 break
                
#                 type = 'Điện thoại'
                
#                 mapping = {
#                     "Công nghệ màn hình": "Màn hình",
#                     "Camera sau": "Camera sau",
#                     "Camera trước": "Camera Selfie",
#                     "Chipset": "CPU",
#                     "Dung lượng RAM": "RAM",
#                     "Bộ nhớ trong": "Bộ nhớ trong",
#                     "Pin": "Pin",
#                     "Thẻ SIM": "Thẻ sim",
#                     "Hệ điều hành": "Hệ điều hành"
#                 }
                
#                 selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.block-content-product > div.block-content-product-right > div > ul > li:nth-child({})'
#                 for i in range(1,11):
#                     try:
#                         pattern = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > p').text
#                         detail = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > div').text
#                         if pattern in mapping:
#                             configDetail[mapping[pattern]] = detail
#                         else: configDetail[pattern] = detail
#                     except NoSuchElementException:
#                         pass
                
#                 productID = 'CPSPHONE' + str(idx + 1000)
#             elif item[2] == 'tablet':
#                 type = 'Máy tính bảng'
                
#                 productID = 'FPTTABLET' + str(idx + 1000)
                
#             promotionDetail = []
#             selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.box-detail-product.columns.m-0 > div.box-detail-product__box-center.column.is-one-third > div:nth-child(4) > div > div.box-product-promotion-content.px-2.pt-2.show-all > div:nth-child({}) > a'
#             for i in range(1,4):
#                 try:
#                     detail = driver.find_element(By.CSS_SELECTOR, selector.format(i)).text
#                     promotionDetail.append(detail)
#                 except NoSuchElementException:
#                     pass 
            
#             featureDetail = []
#             instance = {
#                 'ProductID': productID, 
#                 'ProductName': productName, 
#                 'BrandName': brandName,
#                 'ShopName': shopName,
#                 'ImageLink': imageLink,
#                 'ProductLink': productLink,
#                 'SalePrice': salePrice,
#                 'NormalPrice': normalPrice,
#                 'Type': type,
#                 'FeatureDetail': featureDetail,
#                 'PromotionDetail': promotionDetail
#             }
            
#             process_item(instance)
            
#         idx+=1
            
#         driver.close()