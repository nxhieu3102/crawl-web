from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product

import csv
from time import sleep

import requests
from requests_html import HTMLSession
import re
import time
import json
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import timeit


from store.crawl.pipelines import process_item, feature_process
from store.crawl.CSVprocess import addLinkToCSV, csvToList


def PhongVuUpdateLink():
    sleep(5)
    start_urls = [
        {'link': 'https://phongvu.vn/c/laptop?page={}','type': 'laptop','feature': None, 'maxPage': 25},
        {'link': 'https://phongvu.vn/c/phone-dien-thoai?page={}', 'type': 'dienthoai', 'feature': None, 'maxPage': 1},
        {'link': 'https://phongvu.vn/c/may-tinh-bang?page={}', 'type': 'tablet', 'feature': None, 'maxPage': 1},
        {'link': 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26698&page={}', 'type': 'laptop', 'feature': 'Doanh nhân', 'maxPage': 5},
        {'link': 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26702&page={}', 'type': 'laptop', 'feature': 'Doanh nhân', 'maxPage': 2},
        {'link': 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26695&page={}', 'type': 'laptop', 'feature': 'Gaming', 'maxPage': 4},
        {'link': 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26699&page={}', 'type': 'laptop', 'feature': 'Học sinh - sinh viên', 'maxPage': 5},
        {'link': 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26696&page={}', 'type': 'laptop', 'feature': 'Văn phòng', 'maxPage': 10},
        {'link': 'https://phongvu.vn/c/laptop?attributes.nhucausudung=26697&page={}', 'type': 'laptop', 'feature': 'Thiết kế đồ hoạ', 'maxPage': 2},
    ]
        
    
    for item in start_urls:
        for i in range(1,item['maxPage'] + 1):
            start_url = item['link'].format(i)
            print(start_url)
            path = './store/crawl/links/pv.csv'
            loaded = csvToList(path)
            
            session = HTMLSession()

            response = session.get(start_url)
            response.html.render(timeout=10000)  # render the dynamic content
            soup = BeautifulSoup(response.html.html, 'html.parser')  # parse the HTML
            
            # writer.writerow([price , name , image , link , config])
            links = soup.find_all(class_='css-13w7uog')

            session.close()

            for link in links:
                a = link.find('a')
                href = 'https://phongvu.vn' + a.get('href')
                print(href)
                if item['feature'] is not None:
                    print('hello')
                    feature_process(href,item['feature'])
                else:
                    flag = True
                    for i in loaded:
                        if i[0] == href:
                            flag = False
                            break
                    if flag:
                        addLinkToCSV(path,[href, item['type']])
            session.close()

def PhongVuUpdateProduct():
    sleep(5)
    loaded = csvToList('./store/crawl/links/pv1.csv')
    indx = 0
    while indx < len(loaded):
        if loaded[indx] is None:
            break
        
        #start = timeit.default_timer()
        
        session = HTMLSession()
        #response = session.get(item[0])
        response = session.get(loaded[indx][0])
        response.html.render(timeout=10000)  # render the dynamic content
        soup = BeautifulSoup(response.html.html, 'html.parser')  # parse the HTML
        
        
        product = ''
        flag = True
        try:
            #product = Product.objects.get(ProductLink = item[0])
            product = Product.objects.get(ProductLink = loaded[indx][0])
        except ObjectDoesNotExist:
            flag = False
            
        if flag:
            salePrice = ''
            if soup.find(class_='att-product-detail-latest-price css-z55zyl') != None:
                salePrice = soup.find(class_='att-product-detail-latest-price css-z55zyl').text
            
            normalPrice = salePrice
            if soup.find(class_='att-product-detail-retail-price css-164smgo') != None:
                normalPrice = soup.find(class_='att-product-detail-retail-price css-164smgo').text            
            
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
        #     div = soup.find(class_='css-4kh4rf')
        #     if div != None:
        #         productName = div.text.replace('Liên hệ đặt hàng' , '')
            
                
        #     shopName = 'PhongVu'
        
        #     imageLink = ''
        #     luu = soup.find(class_='css-j4683g')
        #     if luu != None:
        #         div = luu.find('img')
        #         if div != None: imageLink = div['src']
           
        #     productLink = loaded[indx][0]
            
        #     div = soup.find(class_='css-s562go')
        #     if div != None:
        #         div = div.find_all('a')
        #         for div2 in div:
        #             href = 'https://phongvu.vn' + div2.get('href')
        #             flag = True
        #             for prodlink in loaded:
        #                 if prodlink[0] == href:
        #                     flag = False
        #                     break
        #             if flag:
        #                 loaded.append([href,loaded[indx][1]])
        #                 addLinkToCSV('./store/crawl/links/pv.csv',[href,loaded[indx][1]])
            
        #     salePrice = ''
        #     if soup.find(class_='att-product-detail-latest-price css-z55zyl') != None:
        #         salePrice = soup.find(class_='att-product-detail-latest-price css-z55zyl').text
            
        #     normalPrice = salePrice
        #     if soup.find(class_='att-product-detail-retail-price css-164smgo') != None:
        #         normalPrice = soup.find(class_='att-product-detail-retail-price css-164smgo').text            
            
        #     configDetail = {}
        #     type = ''
        #     brandName = ''
        #     if loaded[indx][1] == 'laptop':
        #         div = soup.find(class_='css-17aam1').get_text(separator='<br/>')
        #         arr = div.split('<br/>')

        #         romInfor = 'none'
        #         pinInfor = 'none'

        #         realName= ["CPU", "RAM", "Lưu trữ", "Màn hình", "Hệ điều hành", "Đồ họa", "Pin", "Khối lượng"]
        #         configs = ["CPU", "RAM", "Lưu trữ", "Màn hình", "Hệ điều hành", "Đồ họa", "Pin", "Khối lượng"]

        #         for br in arr:
        #             content = br
        #             content = content.replace('-' , '')
        #             content = content.replace(':' , '')

        #             for i in range(len(configs)):
        #                 if configs[i] in content:
        #                     content = content.replace(configs[i] , '').strip()
        #                     configDetail[realName[i]] = content
                
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
                            
        #         productID = 'PVLAP' + str(indx + 1000)
        #     elif loaded[indx][1] == 'dienthoai':
        #         div = soup.find(class_='css-17aam1').get_text(separator='<br/>')
        #         arr = div.split('<br/>')
        #         # print(arr)

        #         romInfor = 'none'
        #         pinInfor = 'none'

        #         realName= ['Lưu trữ' , "Màn hình" , "Hệ điều hành" , "Pin" , "Camera sau" , "Camera trước"]
        #         configs = ['Bộ nhớ' , "Màn hình" , "Hệ điều hành" , "Pin" , "Camera sau" , "Camera trước"]

        #         for br in arr:
        #             content = br
        #             content = content.replace('-' , '')
        #             content = content.replace(':' , '')

        #             for i in range(len(configs)):
        #                 if configs[i] in content:
        #                     content = content.replace(configs[i] , '').strip()
        #                     configDetail[realName[i]] = content

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
                
        #         productID = 'PVPHONE' + str(indx + 1000)
        #     elif loaded[indx][1] == 'tablet':
        #         div = soup.find(class_='css-17aam1').get_text(separator='<br/>')
        #         arr = div.split('<br/>')
        #         # print(arr)

        #         romInfor = 'none'
        #         pinInfor = 'none'

        #         realName= ['Lưu trữ' , "Màn hình" , "Hệ điều hành" , "Pin" , "Camera sau" , "Camera trước"]
        #         configs = ['Bộ nhớ' , "Màn hình" , "Hệ điều hành" , "Pin" , "Camera sau" , "Camera trước"]


        #         for br in arr:
        #             content = br
        #             content = content.replace('-' , '')
        #             content = content.replace(':' , '')

        #             for i in range(len(configs)):
        #                 if configs[i] in content:
        #                     content = content.replace(configs[i] , '').strip()
        #                     configDetail[realName[i]] = content

        #         type = 'Máy tính bảng'
                
        #         productID = 'PVTABLET' + str(indx + 1000)
                
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
            
        #     print(instance)
        #     process_item(instance)
            
        indx = indx + 1
        session.close()
    
    print("finished updating PhongVu")
#PhongVuUpdateProduct()