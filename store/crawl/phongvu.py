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

def PhongVuUpdateProduct():
    sleep(20)
    loaded = csvToList('./store/links/test3.csv')
    for item in loaded:
        #print(item)
        #start_urls = 'https://fptshop.com.vn/may-tinh-xach-tay/asus-tuf-gaming-fx506lhb-hn188w-i5-10300h'
        driver = webdriver.Chrome(chrome_options=options)
        wait = WebDriverWait(driver, 10)
        
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
            salePrice = driver.find_element(By.CSS_SELECTOR,'.css-1q5zfcu .att-product-detail-latest-price').text
        except NoSuchElementException:
            pass
        
        normalPrice = ''
        try:
            normalPrice = driver.find_element(By.CSS_SELECTOR,'.css-1q5zfcu .att-product-detail-retail-price').text
        except NoSuchElementException:
            pass
        
        if normalPrice != '' and salePrice == '':
            salePrice = normalPrice
        elif normalPrice == '' and salePrice != '':
            normalPrice = salePrice

        #print(salePrice,normalPrice)
        
        try:
            product = Product.objects.get(ProductLink = item[0])
            if salePrice != '' and normalPrice != '':
                product.SalePrice = salePrice
                product.NormalPrice = normalPrice
                addLinkToCSV('./laptop.csv',["updated pv"])
                product.save()
        except ObjectDoesNotExist:
            pass
            
        driver.close()
        
        
        