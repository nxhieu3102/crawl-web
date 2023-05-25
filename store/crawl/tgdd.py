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
import timeit

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

def TGDDUpdateLink():
    sleep(5)
    start_urls = [
        {'link': 'https://www.thegioididong.com/laptop#c=44&o=17&pi=11', 'type': 'laptop','feature': None},
        {'link': 'https://www.thegioididong.com/dtdd#c=42&o=17&pi=5','type': 'dienthoai','feature': None},
        {'link': 'https://www.thegioididong.com/may-tinh-bang#c=522&o=17&pi=1','type': 'tablet', 'feature': None},
        {'link': 'https://www.thegioididong.com/laptop?g=cao-cap-sang-trong#c=44&p=37700&o=17&pi=2', 'type': 'laptop','feature': 'Doanh nhân'},
        {'link': 'https://www.thegioididong.com/laptop?g=laptop-gaming#c=44&p=37699&o=17&pi=2', 'type': 'laptop', 'feature': 'Gaming'},
        {'link': 'https://www.thegioididong.com/laptop?g=hoc-tap-van-phong#c=44&p=37697&o=17&pi=8', 'type': 'laptop', 'feature': 'Học sinh - Sinh viên'},
        {'link': 'https://www.thegioididong.com/laptop?g=do-hoa-ky-thuat#c=44&p=81785&o=17&pi=3', 'type': 'laptop', 'feature': 'Thiết kế đồ hoạ'},
   ]
    
    for item in start_urls:
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
        selector = ''
        if item['type'] == 'laptop':
            selector = '.__cate_44 > a.main-contain'
        elif item['type'] == 'dienthoai':
            selector = '.__cate_42 > a.main-contain'
        elif item['type'] == 'tablet':
            selector = '.__cate_522 > a.main-contain'
            
        try:
            tmp = driver.find_elements(By.CSS_SELECTOR,selector)
        except NoSuchElementException:
            pass
                    
        path = './store/crawl/links/tgdd.csv'
        loaded = csvToList(path)
        
        for var in tmp:
            url = var.get_attribute('href')
            print('hello',url)

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


def TGDDUpdateProduct():
    sleep(5)
    loaded = csvToList('./store/crawl/links/tgdd1.csv')
    indx = 0
    while indx < len(loaded):
        if len(loaded[indx]) == 0:
            break
                
        session = HTMLSession()
        response = session.get(loaded[indx][0])
        response.html.render(timeout=10000)  # render the dynamic content
        soup = BeautifulSoup(response.html.html, 'html.parser')  # parse the HTML
        
        product = ''
        flag = True
        try:
            product = Product.objects.get(ProductLink = loaded[indx][0])
        except ObjectDoesNotExist:
            flag = False
            
        if flag:
            salePrice = ''
            normalPrice = ''
            div = soup.find('div' , class_='box-price')
            if div != None:
                salePrice = div.find('p' , class_='box-price-present').text
                if salePrice is not None and salePrice.endswith('*'):
                    salePrice = salePrice.replace(' *','').strip()
            
                normalPrice = salePrice
                if div.find('p' , class_='box-price-old') != None:
                    normalPrice = div.find('p' , class_='box-price-old').text
                    
            if len(salePrice) > 20:
                if 'Giá dự kiến:' in salePrice:
                    salePrice = salePrice.replace('Giá dự kiến:','')
                    salePrice = salePrice.strip()
                else: salePrice = ''
            
            if len(normalPrice) > 20:
                if 'Giá dự kiến:' in normalPrice:
                    normalPrice = normalPrice.replace('Giá dự kiến:','')
                    normalPrice = normalPrice.strip()
                else: normalPrice = ''
            
            if normalPrice != '' and salePrice == '':
                salePrice = normalPrice
            elif normalPrice == '' and salePrice != '':
                normalPrice = salePrice
            
            if salePrice != '' and normalPrice != '':
                product.SalePrice = salePrice
                product.NormalPrice = normalPrice
                product.save()
                #print(indx,"updated price of ", product.ProductID,product.SalePrice,product.NormalPrice)
        # else:
        #     productID = ''
            
        #     productName = ''
        #     div = soup.find('section' , {'class': 'detail'})
        #     if div != None:
        #         div = div.find('h1')
        #         productName = div.text
                
        #     shopName = 'TGDD'
        
        #     imageLink = ''
        #     luu = soup.find('div' , {'class': 'owl-item active'})
        #     if luu != None:
        #         div = luu.find('img')
        #         if div != None and 'src' in div: 
        #             imageLink = div['src']
            
            
        #     productLink = loaded[indx][0]
            
        #     div = soup.find(class_='box03')
        #     if div != None:
        #         div = div.find_all('a')
        #         for div2 in div:
        #             tmp = div2.get('href')
        #             if not '/dtdd/' in tmp or not '/may-tinh-bang/' in tmp or not '/laptop/' in tmp:
        #                 continue
        #             href = 'https://www.thegioididong.com' + tmp
        #             flag = True
        #             for prodlink in loaded:
        #                 if prodlink[0] == href:
        #                     flag = False
        #                     break
        #             if flag:
        #                 loaded.append([href,loaded[indx][1]])
        #                 addLinkToCSV('./store/crawl/links/tgdd.csv',[href,loaded[indx][1]])
                
        #     salePrice = ''
        #     normalPrice = ''
        #     div = soup.find('div' , class_='box-price')
        #     if div != None:
        #         salePrice = div.find('p' , class_='box-price-present').text
        #         if salePrice is not None and salePrice.endswith('*'):
        #             salePrice = salePrice.replace(' *','').strip()
            
        #         normalPrice = salePrice
        #         if div.find('p' , class_='box-price-old') != None:
        #             normalPrice = div.find('p' , class_='box-price-old').text
                    
        #     if len(salePrice) > 20:
        #         if 'Giá dự kiến:' in salePrice:
        #             salePrice = salePrice.replace('Giá dự kiến:','')
        #             salePrice = salePrice.strip()
        #         else: salePrice = ''
            
        #     if len(normalPrice) > 20:
        #         if 'Giá dự kiến:' in normalPrice:
        #             normalPrice = normalPrice.replace('Giá dự kiến:','')
        #             normalPrice = normalPrice.strip()
        #         else: normalPrice = ''
            
        #     configDetail = {}
        #     type = ''
        #     brandName = ''
        #     if loaded[indx][1] == 'laptop':
        #         type = 'Máy tính cá nhân'
                
        #         if productName:
        #             brands = ['macbook' , 'asus' , 'hp' , 'lenovo' , 'acer' , 'dell' ,
        #                 'msi' , 'surface' , 'itel' , 'masstel' , 'chuwi' , 'lg', 'gigabyte']
        #             for brand in brands:
        #                 if brand.upper() in productName.upper():
        #                     if brand == 'macbook':
        #                         brand = 'APPLE'
        #                     brandName = brand.upper()
        #                     break
                            
        #         productID = 'TGDDLAP' + str(indx + 1000)
        #     elif loaded[indx][1] == 'dienthoai':
        #         if productName:
        #             brands = ['iphone' , 'samsung' , 'oppo' , 'xiaomi' , 'vivo' , 'realme' , 
        #             'nokia' , 'tcl' , 'mobell' , 'itel' , 'masstel']
        #             for brand in brands:
        #                 if brand.upper() in productName.upper():
        #                     if brand == 'iphone':
        #                         brand = 'APPLE'
        #                     brandName = brand.upper()
        #                     break
                
        #         type = 'Điện thoại'
                
        #         productID = 'TGDDPHONE' + str(indx + 1000)
        #     elif loaded[indx][1] == 'tablet':
        #         type = 'Máy tính bảng'
                
        #         productID = 'TGDDTABLET' + str(indx + 1000)
                
        #         if productName:
        #             brands = ['iphone' , 'samsung' , 'oppo' , 'xiaomi' , 'vivo' , 'realme' , 
        #             'nokia' , 'tcl' , 'mobell' , 'itel' , 'masstel']
        #             for brand in brands:
        #                 if brand.upper() in productName.upper():
        #                     if brand == 'iphone':
        #                         brand = 'APPLE'
        #                     brandName = brand.upper()
        #                     break
                        
            
        #     promotionDetail = []     
        #     if soup.find('div' , class_='pr-item') != None:
        #         div = soup.find('div' , class_='pr-item').find_all('p')
        #         for pro in div:
        #             text_content = ''.join(pro.find_all(string=True, recursive=False)).strip()
        #             promotionDetail.append(text_content)
            
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
            
        indx = indx + 1
        session.close()
    
    print("finished updating Thegioididong")
#TGDDUpdateProduct()


        
        
        
        
                