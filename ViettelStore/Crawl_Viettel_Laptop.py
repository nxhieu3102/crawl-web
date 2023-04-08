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
    romInfor = 'none'
    CPUInfor = 'none'
    screenSize = 'none'
    ramInfor = 'none'
    graphCard = 'none'
    for li in div:
        luu = li.find_all('td')
        content = luu[0].text
        if 'Ổ cứng' in content:
            romInfor = luu[1].text
        if 'Bộ vi xử lý' in content:
            CPUInfor = luu[1].text
        if 'Màn hình' in content:
            screenSize = luu[1].text
        if 'Bộ nhớ' in content:
            ramInfor = luu[1].text
        if 'Card đồ họa' in content:
            graphCard = luu[1].text
    return [CPUInfor , ramInfor , romInfor , graphCard , screenSize]

#promote
def GetPromote(soup):
    if soup.find('div' , {'class':'body-promotion'}) == None:
        return []
    elements = soup.find('div' , {'class':'body-promotion'}).text
    content_lines = [line.strip() for line in elements.split("\n") if line.strip()]
    result = [line.replace(", chi tiết\xa0TẠI ĐÂY", "") for line in content_lines]
    result = [line.replace("\xa0", " ") for line in content_lines]
    


    # for i in content_lines:
    #     i = i.replace(', chi tiết\xa0TẠI ĐÂY' , '')
    #     print(i)
    # 6
    # print(result)

    # for element in elements:
    #     print(element)
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
        return ['None' , 'None']
    star = round(sum/sl , 2)
    ratingNum = sl
    return [star , ratingNum]


f = open('.\DataViettelStore\link_LapTop.txt' , 'r')
productLinks = []
for line in f:
    productLinks.append(line.strip())
    
f.close()

# print(len(productLinks))
# for link in productLinks:
#     print(link)


file = open('.\DataViettelStore\link_LapTop.csv', 'a', encoding='utf-8-sig', newline='')
writer = csv.writer(file)
# writer.writerow(['Price(old, present)' , 'Name' , 'Image' , 'Rating(stars, rating number)' , 'Promotion(save as a list)' , 'Link' , 'Configuration(CPU, RAM, ROM, screenCard, screen)'])
for link in productLinks:
    print(link)
    session = HTMLSession()
    # link = 'https://viettelstore.vn/laptop/mtxt-giao-duc-masstel-e116-intel-celeron-n4020-4gb-ram-128gb-emmc-11-6-inch-hd-win-10-pro-grey-pid289222.html'
    # r = requests.get(link , headers = headers)
    # soup = BeautifulSoup(r.content , 'html.parser')
    response = session.get(link)
    response.html.render(timeout=10000)  # render the dynamic content
    soup = BeautifulSoup(response.html.html, 'html.parser')  # parse the HTML
    # print(soup)

    price = getPrice(soup)
    # print(price)
    name = getName(soup)
    image = getImage(soup)
    # print(image)

    rating = getRating(soup)
    # print(rating)
    promote = GetPromote(soup)
    #link
    config = getConfig(soup)
    # print(config)
    writer.writerow([price , name , image , rating , promote , link , config])
    # print([price , name , image , rating , promote , link , config])
    session.close()
    print('Done!\n')


writer.close()