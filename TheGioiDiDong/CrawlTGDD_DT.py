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
    pinInfor = 'none'
    for li in div:
        content = li.find('p').text
        if 'Dung lượng' in content:
            romInfor = li.find('span').text
        if 'Pin' in content:
            pinInfor = li.find('span').text
    return [romInfor , pinInfor]


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
    star = 'None'
    ratingNum = 'None'
    if div.find('p') != None:
        star = div.find('p').text
    if div.find('a') != None:
        ratingNum = div.find('a').text
    return [star , ratingNum]

# r = requests.get('https://www.thegioididong.com/dtdd',
#                 # verify=False,
#                 # params=params,
#                 # proxies=proxies,
#                 headers=headers
# )

f = open('.\dataTGDD\link_DT.txt' , 'r')
productLinks = []
for line in f:
    productLinks.append(line.strip())
    
f.close()


file = open('.\dataTGDD\dienThoai.csv', 'a', encoding='utf-8-sig', newline='')
writer = csv.writer(file)
# writer.writerow(['Price(old, present)' , 'Name' , 'Image' , 'Rating(stars, rating number)' , 'Promotion(save as a list)' , 'Link' , 'Configuration(Rom, Pin)'])
for link in productLinks:
    print(link)
    session = HTMLSession()
    # link = 'https://www.thegioididong.com/dtdd/iphone-14-pro-max'
    # r = requests.get(link , headers = headers)
    # soup = BeautifulSoup(r.content , 'html.parser')
    response = session.get(link)
    response.html.render(timeout=10000)  # render the dynamic content
    soup = BeautifulSoup(response.html.html, 'html.parser')  # parse the HTML
    # time.sleep(2)
    price = getPrice(soup)
    name = getName(soup)
    image = getImage(soup)
    # print(name)

    rating = getRating(soup)
    promote = GetPromote(soup)
    #link
    config = getConfig(soup)
    writer.writerow([price , name , image , rating , promote , link , config])
    session.close()
    print('Done!\n')

# print(price , name , image , rating , promote , link , config)

# writer.close()



















