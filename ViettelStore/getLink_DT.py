# //*[@id="div_Danh_Sach_San_Pham_loadMore_btn_laptophssv"]/a
# /html/body/div[4]/div/div[3]/div[2]/div/div/a
# #div_Danh_Sach_San_Pham_loadMore_btn_laptophssv > a

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import json
import csv

driver_path = '"D:\.EXE\chromedriver_win32\chromedriver.exe"'
driver = webdriver.Chrome(executable_path=driver_path)

#######get all links from main page
driver.get('https://viettelstore.vn/dien-thoai')
time.sleep(5)

while True:
    try:
        button = driver.find_element(By.ID , 'div_Danh_Sach_San_Pham_loadMore_btn')
        print(button)
        if button == None:
            break
        button.click()
        time.sleep(2)
    except:
        break
    
        # extract information from each item


elements = driver.find_elements(By.CLASS_NAME, "ProductList3Col_item")
# print(elements)
file = open('.\DataViettelStore\link_DT.txt', 'w')

for element in elements:
    element_child = element.find_element(By.TAG_NAME, 'a')
    # print(element_child)
    # linkList.append()
    # jsonstring = json.dumps({'link' : element_child.get_attribute('href')})
    file.write(element_child.get_attribute('href')+'\n')
    # jsonFile.write('\n')
    print(element_child.get_attribute('href'))

file.close()

driver.quit()