import requests
from requests_html import HTMLSession
import html
import re
import csv
import time
import json
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings


disable_warnings(InsecureRequestWarning)
baseUrl = 'https://www.thegioididong.com'

headers = {
    # 'Host' : 'free-proxy.cz',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'Referer' : 'http://free-proxy.cz/en/',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    # 'TE': 'Trailers'
}
# proxies = { 
#     'https' : 'https://123.25.21.211:3128' 
# }
params = {
    '__blob': 'publicationFile'
}

#name
def getName(soup):
    div = soup.find('div' , class_='left-li2').find('h1')
    return div.text.strip()
    

# brandName
def findBrand(s):
    brands = ['iphone' , 'samsung' , 'oppo' , 'xiaomi' , 'vivo' , 'realme' ,
                'zte', 'nokia', 'itel' , 'masstel' , 'philips' , 'tecno']
    for brand in brands:
        if brand.upper() in s.upper():
            if brand == 'iphone':
                brand = 'APPLE'
            return brand.upper()
    return None

##image
def getImage(soup):
    img = 'None'
    luu = soup.find('div' , class_="owl-wrapper")
    # print(luu)

    div_element = luu.find('img')
    # print(div_element)
    img = div_element['src']
    # print(img)
    return img

#old price and present price
def getPrice(soup):
    div = soup.find('div' , class_='left-li2')
    if div == None:
        return [None , None]
    # print(div)
    presentPrice = div.find('span' , {'id':'_price_new436'}).text
    # print(presentPrice)
    oldPrice = 'None'
    if div.find('span' , {'id':'_price_new437'}) != None:
        oldPrice = div.find('span' , {'id':'_price_new437'}).text
    # print(oldPrice)
    return [oldPrice , presentPrice]

#cau hinh
def getConfig(soup):
    div = soup.find('tbody').find_all('tr')
    # print(div)
    ConfigPattern = ["Bộ nhớ trong", "Màn hình", "Hệ điều hành", 
                    "Pin", "Camera sau", "Camera trước"]
        
    realName = ["Lưu trữ", "Màn hình", "Hệ điều hành", 
                "Pin", "Camera sau", "Camera trước"]

    item = {}
    for tr in div:
        left = tr.find_all('td')[0].text
        right = tr.find_all('td')[1].text
        for i in range(len(ConfigPattern)):
            if ConfigPattern[i] in left:
                item[realName[i]] = right
    return item

#promote
def GetPromote(soup):
    if soup.find('div' , {'class':'body-promotion'}) == None:
        return []
    elements = soup.find('div' , {'class':'body-promotion'}).text
    content_lines = [line.strip() for line in elements.split("\n") if line.strip()]
    result = [line.replace(", chi tiết TẠI ĐÂY", "") for line in content_lines]
    result = [line.replace("\xa0", " ") for line in result]
    
    return result

#rating
def getRating(soup):
    div = soup.find_all('span' , class_='rating-counter')
    # print(div)
    star = 0
    ratingNum = 0
    sum = 0
    count = 5
    sl = 0
    for i in div:
        sum += int(i.text)*count
        sl += int(i.text)
        count -= 1
    if sum == 0:
        return {'None' , 'None'}
    star = round(sum/sl , 2)
    ratingNum = sl
    return [star , ratingNum]


f = open('ViettelStore\DataViettelStore\link_DT.txt' , 'r')
productLinks = []
for line in f:
    productLinks.append(line.strip())
    
f.close()

# print(len(productLinks))
# for link in productLinks:
#     print(link)


itemList = []
file = open('ViettelStore\DataViettelStore\DT.json', 'a', encoding='utf-8-sig', newline='') 
count = 0
# writer.writerow(['Price(old, present)' , 'Name' , 'Image' , 'Rating(stars, rating number)' , 'Promotion(save as a list)' , 'Link' , 'Configuration(Rom, Pin)'])
for link in productLinks:
    print(count)
    print(link)
    session = HTMLSession()
    response = session.get(link)
    response.html.render(timeout=15000)  # render the dynamic content
    soup = BeautifulSoup(response.html.html, 'html.parser')  # parse the HTML
    # print(soup)

    item = {}

    temp = getPrice(soup)
    item['SalePrice'] = temp[1] #present price
    item['NormalPrice'] = temp[0] #old price
    if temp[1] == None:
        continue
    

    count += 1
    item['ProductID'] = 'VSPHONE' + str(count)
    
    item['ImageLink'] = getImage(soup)

    item['ProductName'] = getName(soup)

    item['ShopName'] = 'Viettel Store'

    item['Type'] = 'Điện thoại'
    
    item['BrandName'] = findBrand(item['ProductName'])

    item['ConfigDetail'] = getConfig(soup)

    item['ProductLink'] = link

    item['PromotionDetail'] = GetPromote(soup)

    # print(item)

    json_str = json.dumps(item)
    file.write(json_str + ',')
    itemList.append(item)

    session.close()
    print('Done!\n')

