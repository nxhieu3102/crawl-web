from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import json
import csv


'''
baseUrl = 'https://www.thegioididong.com/laptop'
tailUrl = [
    '?g=laptop-gaming#c=44&p=37699&o=17&pi=2', 
    '-apple-macbook', 
    '?g=hoc-tap-van-phong#c=44&p=37697&o=17&pi=7', 
    '?g=do-hoa-ky-thuat#c=44&p=81785&o=17&pi=3', 
    '?g=mong-nhe-thoi-trang#c=44&p=37698&o=17&pi=1',
    '?g=cao-cap-sang-trong#c=44&p=37700&o=17&pi=2'
]
'''

#######get all links from main page

#for tail in tailUrl:
driver_path = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)
_url = 'https://www.thegioididong.com/laptop#c=44&o=17&pi=10'
driver.get(_url)
time.sleep(4)

elements = driver.find_elements(By.CLASS_NAME, "__cate_44")
# print(elements)
file = open('TGDDLaptopLink.json', 'a')

for element in elements:
    element_child = element.find_elements(By.TAG_NAME, 'a')[0] 
    # linkList.append()
    # jsonstring = json.dumps({'link' : element_child.get_attribute('href')})
    # jsonFile.write('\n')
    instance = {}
    instance['ProductLink'] = element_child.get_attribute('href')
    tmp = json.dumps(instance)
    file.write(tmp)
    

file.close()

driver.quit()