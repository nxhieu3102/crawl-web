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

#######get all links from main page

#for tail in tailUrl:
driver_path = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)
_url = 'https://www.thegioididong.com/dtdd#c=42&o=17&pi=5'
driver.get(_url)
time.sleep(5)

elements = driver.find_elements(By.CLASS_NAME, "__cate_44")
# print(elements)
file = open('TGDDPhoneLink.json', 'a')

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
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import json
import csv

driver_path = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)

#######get all links from main page
driver.get('https://www.thegioididong.com/may-tinh-bang#c=522&o=17&pi=1')
time.sleep(5)

#file = open('.\dataTGDD\link_DT.txt', 'w')
elements = driver.find_elements(By.CLASS_NAME, "__cate_522")

file = open('TGDDTabletLink.json', 'a')

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
'''
import json
import csv

loaded = ''
with open('abc.json','r') as file:
    loaded = json.load(file)

res = []
tmp = []
for i in range(len(loaded)):
    if loaded[i]['ProductLink'] not in tmp:
        tmp.append(loaded[i]['ProductLink'])

        res.append([loaded[i]['ProductLink']])
            
#fieldnames = res[0].keys()
print(len(res))
header = ['ProductLink']
    # Write the list of dictionaries to the CSV file
with open('laptoplink.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)  # Write the fieldnames as the first row (header) in the CSV file
    writer.writerows(res)  # Write the data rows to the CSV file
