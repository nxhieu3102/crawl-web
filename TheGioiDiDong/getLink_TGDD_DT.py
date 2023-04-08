from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import json
import csv

driver_path = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)

#######get all links from main page
driver.get('https://www.thegioididong.com/dtdd#c=42&o=17&pi=5')
time.sleep(5)

elements = driver.find_elements(By.CLASS_NAME, "__cate_42")
file = open('.\dataTGDD\link_DT.txt', 'w')

for element in elements:
    element_child = element.find_elements(By.TAG_NAME, 'a')[0] 
    # linkList.append()
    # jsonstring = json.dumps({'link' : element_child.get_attribute('href')})
    file.write(element_child.get_attribute('href')+'\n')
    # jsonFile.write('\n')
    print(element_child.get_attribute('href'))

file.close()

driver.quit()