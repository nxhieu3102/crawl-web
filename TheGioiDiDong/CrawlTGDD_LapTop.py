import requests
from requests_html import HTMLSession
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
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
}
params = {
    '__blob': 'publicationFile'
}

#name
def getName(soup):
    div = soup.find('section' , {'class': 'detail'}).find('h1')
    return div.text
    

##image
def getImage(soup):
    img = 'None'
    # temp = soup.find_all('div' , {'class': 'owl-item active'})
    # print(temp)
    # div = temp[0]
    # img = div.find('img')['src']
    # print(soup)
    # print(soup.find('div' , {'class': 'owl-item active'}))
    luu = soup.find('div' , {'class': 'owl-item active'}).find('img')
    if luu != None:
        div = luu
        img = div['src']
    return img

#old price and present price
def getPrice(soup):
    div = soup.find('div' , class_='box-price')
    presentPrice = div.find('p' , class_='box-price-present').text
    oldPrice = 'None'
    if div.find('p' , class_='box-price-old') != None:
        oldPrice = div.find('p' , class_='box-price-old').text
    return [oldPrice , presentPrice]


#cau hinh
def getConfig(soup):
    div = soup.find('div' , class_='parameter').find_all('li')
    romInfor = 'none'
    CPUInfor = 'none'
    RAMInfor = 'none'
    screenCard = 'None'
    screen = 'None'
    for li in div:
        content = li.find('p').text
        if 'Ổ cứng' in content:
            temp = li.find_all('span')
            romInfor = ''
            for i in temp:
                romInfor += (i.text + ', ')
        elif 'CPU' in content:
            temp = li.find_all('span')
            CPUInfor = ''
            for i in temp:
                CPUInfor += (i.text + ', ')
        elif 'RAM' in content:
            temp = li.find_all('span')
            RAMInfor = ''
            for i in temp:
                RAMInfor += (i.text + ', ')
        elif 'Card màn hình' in content:
            temp = li.find_all('span')
            screenCard = ''
            for i in temp:
                screenCard += (i.text + ', ')
        elif 'Màn hình' in content:
            temp = li.find_all('span')
            screen = ''
            for i in temp:
                screen += (i.text + ', ')
        
    return [CPUInfor[:-2], RAMInfor[:-2], romInfor[:-2], screenCard[:-2], screen[:-2]]


#promote
def GetPromote(soup):
    if soup.find('div' , class_='pr-item') == None:
        return []
    div = soup.find('div' , class_='pr-item').find_all('p')
    promoteList = []
    # print(div)
    for pro in div:
        text_content = ''.join(pro.find_all(string=True, recursive=False)).strip()
        promoteList.append(text_content)
    return promoteList

#rating
def getRating(soup):
    div = soup.find('div' , class_='rating-top')
    if div == None:
        return ['None' , 'None']
    star = 'None'
    ratingNum = 'None'
    if div.find('p') != None:
        star = div.find('p').text
    if div.find('a') != None:
        ratingNum = div.find('a').text
    return [star , ratingNum]

# session = HTMLSession()
# response = session.get('https://www.thegioididong.com/dtdd')
# response.html.render()  # render the dynamic content
# soup = BeautifulSoup(response.html.html, 'html.parser')  # parse the HTML
# productList = soup.find_all('li' , {'class': 'item ajaxed __cate_42'})
# print(soup)
# time.sleep(5)
# print(productList)


# for item in productList:
#     for link in item.find_all('a' , {'class' : 'main-contain'}):
#         productLinks.append(baseUrl + link['href'])
#         # print(baseUrl + link['href'])


f = open('.\dataTGDD\link_LapTop.txt' , 'r')
productLinks = []
for line in f:
    productLinks.append(line.strip())
    
f.close()


file = open('.\dataTGDD\Laptop.csv', 'a', encoding='utf-8-sig', newline='')
writer = csv.writer(file)
# writer.writerow([
#     'Price(old, present)', 
#     'Name' , 'Image', 
#     'Rating(stars, rating number)', 
#     'Promotion(save as a list)', 
#     'Link', 
#     'Configuration(CPU, RAM, ROM, screenCard, screen)'
# ])

for link in productLinks:
    print(link)
    session = HTMLSession()
    # link = 'https://www.thegioididong.com/laptop/hp-15s-du1108tu-i3-10110u-2z6l7pa'
    response = session.get(link)
    response.html.render(timeout=10000)  # render the dynamic content
    soup = BeautifulSoup(response.html.html, 'html.parser')  # parse the HTML
    # time.sleep(2)

    # print(soup.find('div' , {'class' : 'box04 notselling'}))
    if soup.find('div' , {'class' : 'box04 notselling'}) != None:
        print('Stop selling')
        continue

    price = getPrice(soup)
    name = getName(soup)
    image = getImage(soup)
    rating = getRating(soup)
    promote = GetPromote(soup)
    #link
    config = getConfig(soup)
    writer.writerow([price , name , image , rating , promote , link , config])

    session.close()
    print('Done!\n')

# print(price , name , image , rating , promote , link , config , end = "\n")

# writer.close()



















