from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
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



def CellPhoneSUpdateLink():
    sleep(5)
    start_urls = [
        {'link': 'https://cellphones.com.vn/laptop.html','type': 'laptop'},
        {'link': 'https://cellphones.com.vn/mobile.html','type': 'dienthoai'},
        {'link': 'https://cellphones.com.vn/tablet.html', 'type': 'tablet'}
    ]
    
    for item in start_urls:
                  
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        
        try:
            driver.get(item['link'])
        except WebDriverException:
            break
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                driver.implicitly_wait(10)
                a_tag = driver.find_element(By.CSS_SELECTOR,'#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a')
                driver.execute_script("arguments[0].click();", a_tag)
            except:
                break
                
        try:
            tmp = driver.find_elements(By.CSS_SELECTOR,'.product-info-container .product-info .product__link')
        except NoSuchElementException:
            pass
        
        path = './store/crawl/links/cps.csv'
        loaded = csvToList(path)
        
        for var in tmp:
            url = var.get_attribute('href')
            flag = True
            for i in loaded:
                if i[0] == url:
                    flag = False
                    break
            if flag:
                addLinkToCSV(path,[url, item['type']])
            
        driver.close()
        
def CellPhoneSUpdateProduct():
    sleep(5)
    loaded = csvToList('./store/crawl/links/cps1.csv')
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
            salePrice = ''
            normalPrice = ''
            
            session = HTMLSession()

            response = session.get(loaded[indx][0])
            response.html.render(timeout=10000)  # render the dynamic content
            soup = BeautifulSoup(response.html.html, 'html.parser')  # parse the HTML

            div = soup.find(class_='product__price--show')
            if div != None:
                salePrice = div.text
                normalPrice = salePrice

                div = soup.find(class_='product__price--through')
                if div != None:
                    normalPrice = div.text

                salePrice = salePrice.strip()
                normalPrice = normalPrice.strip()
                print("hello")
    
            session.close()
            
            if normalPrice != '' and salePrice == '':
                salePrice = normalPrice
            elif normalPrice == '' and salePrice != '':
                normalPrice = salePrice
            
            if salePrice != '' and normalPrice != '':
                product.SalePrice = salePrice
                product.NormalPrice = normalPrice
                product.save()
                #print(indx,"updated price of ", product.ProductID, product.SalePrice, product.NormalPrice)
        # else:
        #     driver = webdriver.Chrome(options=options)
        #     wait = WebDriverWait(driver, 10)
            
        #     try:
        #         driver.get(loaded[indx][0])
        #     except WebDriverException:
        #         break
            
        #     check_height = driver.execute_script("return document.body.scrollHeight;")
        #     while True:
        #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #         try:
        #             wait.until(lambda driver: driver.execute_script("return document.body.scrollHeight;")  > check_height)
        #             check_height = driver.execute_script("return document.body.scrollHeight;") 
        #         except:
        #                 break
            
        #     productID = ''
        #     productName = ''
        #     try:
        #         productName = driver.find_element(By.CSS_SELECTOR,'div.box-product-name > h1').text.strip()
        #     except NoSuchElementException:
        #         pass
                
        #     shopName = 'CellPhoneS'
        
        #     imageLink = ''
        #     try:
        #         imageLink = driver.find_element(By.XPATH,'//*[@id="layout-desktop"]/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/img').get_attribute('src')
        #     except NoSuchElementException:
        #         pass
            
        #     productLink = loaded[indx][0]
            
        #     salePrice = ''
        #     try:
        #         salePrice = driver.find_element(By.CSS_SELECTOR,'.product__price--show').text
        #     except NoSuchElementException:
        #         pass
            
        #     normalPrice = salePrice
        #     try:
        #         normalPrice = driver.find_element(By.CSS_SELECTOR,'.product__price--through').text
        #     except NoSuchElementException:
        #         pass
            
        #     for idx in range(2,5):
        #         try:
        #             link = '#productDetailV2 > section > div.box-detail-product.columns.m-0 > div.box-detail-product__box-center.column > div.box-linked > div > a:nth-child({})'
        #             link = link.format(idx)
        #             i = driver.find_element(By.CSS_SELECTOR, link).get_attribute('href')
        #             flag = True
        #             for prodlink in loaded:
        #                 if prodlink[0] == i:
        #                     flag = False
        #                     break
        #             if flag:
        #                 loaded.append([i,loaded[indx][1]])
        #                 addLinkToCSV('./store/crawl/links/cps.csv',[i,loaded[indx][1]])
        #         except NoSuchElementException:
        #             pass
            
        #     configDetail = {}
        #     type = ''
        #     brandName = ''
        #     if loaded[indx][1] == 'laptop':
        #         mapping = {
        #             "Loại card đồ họa": "Đồ họa",
        #             "Dung lượng RAM": "RAM",
        #             "Ổ cứng": "Lưu trữ",
        #             "Công nghệ màn hình": "Màn hình",
        #             "Pin": "Pin",
        #             "Hệ điều hành": "Hệ điều hành",
        #         }
                
        #         selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.block-content-product > div.block-content-product-right > div > ul > li:nth-child({})'
        #         for i in range(1,11):
        #             try:
        #                 pattern = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > p').text
        #                 detail = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > div').text
        #                 #for key in mapping.keys():
        #                     #if pattern == key:
        #                 if pattern in mapping:
        #                     configDetail[mapping[pattern]] = detail
        #                 else: configDetail[pattern] = detail
        #             except NoSuchElementException:
        #                 pass
                    
        #         type = 'Máy tính cá nhân'
                
        #         try:
        #             brandName = driver.find_element(By.CSS_SELECTOR,'#breadcrumbs > div.block-breadcrumbs.affix > div > ul > li:nth-child(3) > a').text.upper()
        #             if brandName == 'MAC':
        #                 brandName = 'APPLE'
        #         except NoSuchElementException:
        #             if productName:
        #                 brands = ['macbook' , 'asus' , 'hp' , 'lenovo' , 'acer' , 'dell' ,
        #                     'msi' , 'surface' , 'itel' , 'masstel' , 'chuwi' , 'lg']
        #                 for brand in brands:
        #                     if brand.upper() in productName.upper():
        #                         if brand == 'macbook':
        #                             brand = 'APPLE'
        #                         brandName = brand.upper()
        #                         break
                            
        #         productID = 'CPSLAP' + str(indx + 1000)
        #     elif loaded[indx][1] == 'dienthoai':
        #         try:
        #             brandName = driver.find_element(By.CSS_SELECTOR,'#breadcrumbs > div.block-breadcrumbs.affix > div > ul > li:nth-child(3) > a').text.upper()
        #         except NoSuchElementException:
        #             if productName:
        #                 brands = ['ipad' , 'samsung' , 'oppo' , 'xiaomi' ,
        #                     'nokia' , 'masstel', 'lenovo']
        #                 for brand in brands:
        #                     if brand.upper() in productName.upper():
        #                         if brand == 'ipad':
        #                             brand = 'APPLE'
        #                         brandName = brand.upper()
        #                         break
                
        #         type = 'Điện thoại'
                
        #         mapping = {
        #             "Công nghệ màn hình": "Màn hình",
        #             "Camera sau": "Camera sau",
        #             "Camera trước": "Camera Selfie",
        #             "Chipset": "CPU",
        #             "Dung lượng RAM": "RAM",
        #             "Bộ nhớ trong": "Bộ nhớ trong",
        #             "Pin": "Pin",
        #             "Thẻ SIM": "Thẻ sim",
        #             "Hệ điều hành": "Hệ điều hành"
        #         }
                
        #         selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.block-content-product > div.block-content-product-right > div > ul > li:nth-child({})'
        #         for i in range(1,11):
        #             try:
        #                 pattern = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > p').text
        #                 detail = driver.find_element(By.CSS_SELECTOR, selector.format(i) + ' > div').text
        #                 if pattern in mapping:
        #                     configDetail[mapping[pattern]] = detail
        #                 else: configDetail[pattern] = detail
        #             except NoSuchElementException:
        #                 pass
                
        #         productID = 'CPSPHONE' + str(indx + 1000)
        #     elif loaded[indx][1] == 'tablet':
        #         type = 'Máy tính bảng'
                
        #         productID = 'FPTTABLET' + str(indx + 1000)
                
        #     promotionDetail = []
        #     selector = '#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > section > div > div.box-detail-product.columns.m-0 > div.box-detail-product__box-center.column.is-one-third > div:nth-child(4) > div > div.box-product-promotion-content.px-2.pt-2.show-all > div:nth-child({}) > a'
        #     for i in range(1,4):
        #         try:
        #             detail = driver.find_element(By.CSS_SELECTOR, selector.format(i)).text
        #             promotionDetail.append(detail)
        #         except NoSuchElementException:
        #             pass 
            
        #     instance = {
        #         'ProductID': productID, 
        #         'ProductName': productName, 
        #         'BrandName': brandName,
        #         'ShopName': shopName,
        #         'ImageLink': imageLink,
        #         'ProductLink': productLink,
        #         'SalePrice': salePrice,
        #         'NormalPrice': normalPrice,
        #         'Type': type,
        #         'PromotionDetail': promotionDetail,
        #         'ConfigDetail': configDetail
        #     }
            
        #     process_item(instance)
            
        #     driver.close()
            
        indx += 1
    
    print("finished updating CellPhoneS")
        
#CellPhoneSUpdateProduct()         
