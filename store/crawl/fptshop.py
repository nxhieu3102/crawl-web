from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options

from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product

import csv
from time import sleep
import re

from store.crawl.pipelines import process_item, feature_process
from store.crawl.CSVprocess import addLinkToCSV, csvToList

import requests
from requests_html import HTMLSession
import re
import time
import json
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

import timeit
        
    
# def rewriteList(fileLink, productLink):
#     with open(fileLink,'w') as fd:
#         for item in productLink:
#             writer = csv.writer(fd)
#             writer.writerow(productLink)
    
# def FPTShopUpdateProduct():
#     sleep(5)
#     loaded = csvToList('./store/links/test1.csv')
#     for item in loaded:
#         #print(item)
#         #start_urls = 'https://fptshop.com.vn/may-tinh-xach-tay/asus-tuf-gaming-fx506lhb-hn188w-i5-10300h'
#         driver = webdriver.Chrome(chrome_options=options)
#         wait = WebDriverWait(driver, 10)
        
#         # try:
#         #     driver.get(item[0])
#         # except WebDriverException:
#         #     break
#         print(item[0])
#         try:
#             driver.set_page_load_timeout(60)
#             driver.get(item[0])
#         except TimeoutException:
#             print("time out")
#             driver.close()
#             break
        
#         check_height = driver.execute_script("return document.body.scrollHeight;")
#         while True:
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             try:
#                 wait.until(lambda driver: driver.execute_script("return document.body.scrollHeight;")  > check_height)
#                 check_height = driver.execute_script("return document.body.scrollHeight;") 
#             except:
#                     break
        
#         salePrice = ''
#         try:
#             salePrice = driver.find_element(By.CSS_SELECTOR, 'div.st-price > div > div.st-price-main').text
#         except NoSuchElementException:
#             pass
        
#         normalPrice = ''
#         try:
#             normalPrice = driver.find_element(By.CSS_SELECTOR, 'div.st-price > div > div.st-price-sub > strike').text
#         except NoSuchElementException:
#             pass
        
#         if normalPrice != '' and salePrice == '':
#             salePrice = normalPrice
#         elif normalPrice == '' and salePrice != '':
#             normalPrice = salePrice

#         print(salePrice,normalPrice)
#         try:
#             product = Product.objects.get(ProductLink = item[0])
#             if salePrice != '' and normalPrice != '':
#                 product.SalePrice = salePrice
#                 product.NormalPrice = normalPrice
#                 addLinkToCSV('./laptop.csv',["updated",item,salePrice,normalPrice])
#                 print("update ", product.ProductID)
#                 product.save()
#             else: addLinkToCSV('./laptop.csv',["checked",item,salePrice,normalPrice])
#         except ObjectDoesNotExist:
#             pass
            
#         driver.close()
def FPTShopUpdateLink():
    sleep(5)
    start_urls = [
        {'link': 'https://fptshop.com.vn/may-tinh-xach-tay?sort=ban-chay-nhat&trang=9', 'type': 'laptop','feature': None},
        {'link': 'https://fptshop.com.vn/dien-thoai?sort=ban-chay-nhat&trang=4','type': 'dienthoai','feature': None},
        {'link': 'https://fptshop.com.vn/may-tinh-bang?sort=ban-chay-nhat&trang=2','type': 'tablet', 'feature': None},
        {'link': 'https://fptshop.com.vn/may-tinh-xach-tay/doanh-nhan?sort=ban-chay-nhat&trang=3', 'type': 'laptop','feature': 'Doanh nhân'},
        {'link': 'https://fptshop.com.vn/may-tinh-xach-tay/gaming-do-hoa?sort=ban-chay-nhat&trang=2', 'type': 'laptop', 'feature': 'Gaming'},
        {'link': 'https://fptshop.com.vn/may-tinh-xach-tay/sinh-vien-van-phong?sort=ban-chay-nhat&trang=5', 'type': 'laptop', 'feature': 'Học sinh - Sinh viên'},
        {'link': 'https://fptshop.com.vn/may-tinh-xach-tay/thiet-ke?sort=ban-chay-nhat&trang=2', 'type': 'laptop', 'feature': 'Thiết kế đồ hoạ'},
   ]
    
    for item in start_urls:
        print(item)
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        
        try:
            driver.get(item['link'])
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
                
        try:
            tmp = driver.find_elements(By.CSS_SELECTOR,'.cdt-product__info .cdt-product__name')
        except NoSuchElementException:
            pass
                    
        path = './store/crawl/links/fpt.csv'
        loaded = csvToList(path)
        
        for var in tmp:
            url = var.get_attribute('href')
            if item['feature']:
                feature_process(url,item['feature'])
            else:
                flag = True
                for i in loaded:
                    if i[0] == url:
                        flag = False
                        break
                if flag:
                    addLinkToCSV(path,[url, item['type']])
        
        driver.close()    

def FPTShopUpdateProduct():
    sleep(5)
    loaded = csvToList('./store/crawl/links/fpt1.csv')
    indx = 0
    while indx < len(loaded):
        if loaded[indx] is None:
            break
        
        product = ''
        flag = True
        try:
            product = Product.objects.get(ProductLink = loaded[indx][0])
        except ObjectDoesNotExist:
            flag = False
            
        if flag:
            session = HTMLSession()

            response = session.get(loaded[indx][0])
            response.html.render(timeout=10000)  # render the dynamic content
            soup = BeautifulSoup(response.html.html, 'html.parser')  # parse the HTML

            salePrice = ''
            normalPrice = ''
            div = soup.find(class_='st-price-main')
            if div != None:
                salePrice = div.text
                normalPrice = salePrice

            div = soup.find(class_='st-price-sub')
            if div != None:
                if div.find('strike') != None:
                    normalPrice = div.find('strike').text
        
            if normalPrice != '' and salePrice == '':
                salePrice = normalPrice
            elif normalPrice == '' and salePrice != '':
                normalPrice = salePrice
            
            if salePrice != '' and normalPrice != '':
                product.SalePrice = salePrice
                product.NormalPrice = normalPrice
                product.save()
                #print(indx,"updated price of ", product.ProductID, product.SalePrice, product.NormalPrice)
        
            session.close()
        indx += 1
    #    else:
    #         driver = webdriver.Chrome(options=options)
    #         wait = WebDriverWait(driver, 5)
            
    #         try:
    #             driver.get(loaded[indx][0])
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
        
    #         productID = ''
    #         productName = ''
    #         try:
    #             productName = driver.find_element(By.CSS_SELECTOR, '.st-name').text
    #             pattern = r'\(.*?\)'
    #             productName = re.sub(pattern,'',productName)
    #         except NoSuchElementException:
    #             pass
                
    #         shopName = 'FPTShop'
        
    #         imageLink = ''
    #         try:
    #             imageLink = driver.find_element(By.CSS_SELECTOR, 'div.swiper-slide.swiper-slide-active > img').get_attribute('src')
    #         except NoSuchElementException:
    #             pass
            
    #         productLink = loaded[indx][0]
            
    #         for idx in range(2,5):
    #             try:
    #                 link = '#root > main > div > div.l-pd-header > div:nth-child(2) > div.l-pd-row.clearfix > div.l-pd-right > div.st-select > a:nth-child({})'
    #                 link = link.format(idx)
    #                 i = driver.find_element(By.CSS_SELECTOR, link).get_attribute('href')
    #                 flag = True
    #                 for prodlink in loaded:
    #                     if prodlink[0] == i:
    #                         flag = False
    #                         break
    #                 if flag:
    #                     loaded.append([i,loaded[indx][1]])
    #                     addLinkToCSV('./store/crawl/links/fpt.csv',[i,loaded[indx][1]])
    #             except NoSuchElementException:
    #                 pass
            
    #         salePrice = ''
    #         try:
    #             salePrice = driver.find_element(By.CSS_SELECTOR, 'div.st-price > div > div.st-price-main').text
    #         except NoSuchElementException:
    #             pass
            
    #         normalPrice = salePrice
    #         try:
    #             normalPrice = driver.find_element(By.CSS_SELECTOR, 'div.st-price > div > div.st-price-sub > strike').text
    #         except NoSuchElementException:
    #             pass
            
    #         configDetail = {}
    #         type = ''
    #         brandName = ''
    #         if loaded[indx][1] == 'laptop':
    #             mapping = {
    #                 "Màn hình": "Màn hình",
    #                 "CPU": "CPU",
    #                 "RAM": "RAM",
    #                 "Ổ cứng": "Lưu trữ",
    #                 "Đồ họa": "Đồ họa",
    #                 "Hệ điều hành": "Hệ điều hành",
    #                 "Trọng lượng": "Khối lượng",
    #                 "Kích thước": "Kích thước"
    #             }
    #             selector = '#root > main > div > div.l-pd-body > div > div.l-pd-body__wrapper > div.l-pd-body__right > div.card.re-card.st-card > div > table > tbody > tr:nth-child({})'
    #             for i in range(1,8):
    #                 try:
    #                     pattern = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > td:nth-child(1)').text
    #                     detail = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > td:nth-child(2)').text
    #                     if pattern in mapping:
    #                         configDetail[mapping[pattern]] = detail
    #                     else: configDetail[pattern] = detail
    #                 except NoSuchElementException:
    #                     pass
                    
    #             type = 'Máy tính cá nhân'
                
    #             try:
    #                 brandName = driver.find_element(By.CSS_SELECTOR, 'li.breadcrumb-item.active > a').text
    #                 brandName = brandName.upper()
    #             except NoSuchElementException:
    #                 if productName:
    #                     brands = ['macbook' , 'asus' , 'hp' , 'lenovo' , 'acer' , 'dell' ,
    #                         'msi' , 'surface' , 'itel' , 'masstel' , 'chuwi' , 'lg', 'gigabyte']
    #                     for brand in brands:
    #                         if brand.upper() in productName.upper():
    #                             if brand == 'macbook':
    #                                 brand = 'APPLE'
    #                             brandName = brand.upper()
    #                             break
                            
    #             productID = 'FPTLAP' + str(idx + 1000)
    #         elif loaded[indx][1] == 'dienthoai':
    #             try:
    #                 brandName = driver.find_element(By.CSS_SELECTOR, 'li.breadcrumb-item.active > a').text.upper()
    #             except NoSuchElementException:
    #                 pass
    #             if productName:
    #                 brands = ['iphone' , 'samsung' , 'oppo' , 'xiaomi' , 'vivo' , 'realme' , 
    #                 'nokia' , 'tcl' , 'mobell' , 'itel' , 'masstel']
    #                 for brand in brands:
    #                     if brand.upper() in productName.upper():
    #                         if brand == 'iphone':
    #                             brand = 'APPLE'
    #                         brandName = brand.upper()
    #                         break
                
    #             type = 'Điện thoại'
                
    #             mapping = {
    #                 "Bộ nhớ trong": "Lưu trữ",
    #                 "Màn hình": "Màn hình",
    #                 "Hệ điều hành": "Hệ điều hành",
    #                 "Pin": "Pin",
    #                 "Camera sau": "Camera sau",
    #                 "Camera Selfie": "Camera trước"
    #             }

    #             selector = '#root > main > div > div.l-pd-body > div > div.l-pd-body__wrapper > div.l-pd-body__right > div:nth-child(1) > div > table > tbody > tr:nth-child({})'
    #             for i in range(1,10):
    #                 try:
    #                     pattern = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > td:nth-child(1)').text
    #                     detail = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > td:nth-child(2)').text
    #                     if pattern in mapping:
    #                         configDetail[mapping[pattern]] = detail
    #                     else: configDetail[pattern] = detail
    #                 except NoSuchElementException:
    #                     pass
                
    #             productID = 'FPTPHONE' + str(indx + 1000)
    #         elif loaded[indx][1] == 'tablet':
    #             type = 'Máy tính bảng'
                
    #             productID = 'FPTTABLET' + str(indx + 1000)
                
    #             try:
    #                 brandName = driver.find_element(By.CSS_SELECTOR, 'li.breadcrumb-item.active > a').text.upper()
    #             except NoSuchElementException:
    #                 pass
    #             if productName:
    #                 brands = ['iphone' , 'samsung' , 'oppo' , 'xiaomi' , 'vivo' , 'realme' , 
    #                 'nokia' , 'tcl' , 'mobell' , 'itel' , 'masstel']
    #                 for brand in brands:
    #                     if brand.upper() in productName.upper():
    #                         if brand == 'iphone':
    #                             brand = 'APPLE'
    #                         brandName = brand.upper()
    #                         break
                
    #         selector = '#root > main > div > div.l-pd-header > div:nth-child(2) > div.l-pd-row.clearfix > div.l-pd-right > div.st-boxPromo > ul > li:nth-child({}) > div > span'
    #         promotionDetail = []
    #         for i in range(1,4):
    #             try:
    #                 detail = driver.find_element(By.CSS_SELECTOR, selector.format(i)).text
    #                 promotionDetail.append(detail)
    #             except NoSuchElementException:
    #                 pass 
            
    #         instance = {
    #             'ProductID': productID, 
    #             'ProductName': productName, 
    #             'BrandName': brandName,
    #             'ShopName': shopName,
    #             'ImageLink': imageLink,
    #             'ProductLink': productLink,
    #             'SalePrice': salePrice,
    #             'NormalPrice': normalPrice,
    #             'Type': type,
    #             'PromotionDetail': promotionDetail,
    #             'ConfigDetail': configDetail
    #         }
            
    #         process_item(instance)
            
    #         driver.close()

            
    #     indx = indx + 1
        
    print("finished updating FPTShop")

#FPTShopUpdateProduct()
 
            