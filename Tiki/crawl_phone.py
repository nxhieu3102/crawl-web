from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
LINK = 'https://tiki.vn/dien-thoai-smartphone/c1795'

driver_path = 'msedgedriver.exe'
driver = webdriver.Edge(executable_path=driver_path)
driver.get(LINK)
LINK_FILE = "phone_link.txt"
DATA_FILE = "phone_data.csv"

# product__price--show
# box-product-name
# technical-content

time.sleep(3)

# click a tag until it is not clickable


def click_a_tag_until_not_clickable():
    while True:
        try:
            time.sleep(1.5)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            a_tag = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div/div[7]/div[5]/div/div[2]/a")
            print(a_tag)
            print(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            driver.execute_script("arguments[0].click();", a_tag)
            if not a_tag:
                break

            # scroll to bottom
        except Exception as e:
            print(e)
            break


def get_phone_link():
    href_list = []
    for i in range(0, 15):
        page_num = i + 1
        new_link = LINK + "?page=" + str(page_num)
        driver.get(new_link)
        time.sleep(2)
        elements = driver.find_elements(By.CLASS_NAME, "product-item")
        href_list_page = [element.get_attribute(
            'href') for element in elements]
        href_list.extend(href_list_page)

    f = open(LINK_FILE, "w+", encoding="utf-8")
    f.write("\n".join(href_list))


def get_phone_data():
    f = open(LINK_FILE, "r+", encoding="utf-8")
    f_csv = open(DATA_FILE, "w+", encoding="utf-8")
    writer = csv.writer(f_csv)
    writer.writerow(["Name", "Price", "Price_Origin", "LINK", "IMG", "RATING"])

    href_list = f.readlines()

    for href in href_list:
        driver.get(href)
        time.sleep(2)
        if driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/main/div[3]/div[1]/div[3]/div[1]/h1") == []:
            continue
        name = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[1]/main/div[3]/div[1]/div[3]/div[1]/h1").text

        price = driver.find_elements(
            By.CLASS_NAME, "product-price__current-price")
        if price == []:
            price = driver.find_elements(
                By.CLASS_NAME, "styles__Price-sc-6hj7z9-1")
            if price == []:
                price = driver.find_elements(By.CLASS_NAME, "flash-sale-price")

        price = price[0].text

        price_origin = driver.find_elements(
            By.CLASS_NAME, "styles__OriginalPrice-sc-6hj7z9-2")

        if price_origin == []:
            price_origin = driver.find_elements(
                By.CLASS_NAME, "list-price")
            if price_origin == []:
                price_origin = driver.find_elements(
                    By.CLASS_NAME, "product-price__list-price")
                
        if price_origin == []:
            price_origin = "None"
        else:
            price_origin = price_origin[0].text

        # /html/body/div[1]/div[1]/main/div[3]/div[1]/div[1]/div[1]/div[1]/div/div/div/picture/img
        # /html/body/div[1]/div[1]/main/div[3]/div[1]/div[1]/div[1]/div[1]/div/div/div/picture/img
        img = driver.find_elements(
            By.XPATH, "/html/body/div[1]/div[1]/main/div[3]/div[1]/div[1]/div[2]/div/a[1]/picture/img")

        if img == []:
            img = driver.find_elements(
                By.XPATH, "/html/body/div[1]/div[1]/main/div[3]/div[1]/div[1]/div[2]/div/a[3]/picture/img")
        if img == []: 
            continue
        img = img[0].get_attribute('src')
        rating = driver.find_elements(
            By.CLASS_NAME, "review-rating__point")

        if rating == []:
            rating = "None"
        else:
            rating = rating[0].text

        # ["Name", "Price", "Price_Origin", "CPU", "RAM",
            # "ROM", "CARD màn hình", "size màn hình", "LINK", "IMG", "RATING"]
        writer.writerow([name, price, price_origin, href, img, rating])

        print(name, price, price_origin, href, img, rating)

    f.close()
    f_csv.close()


    # write data above to csv file
# click_a_tag_until_not_clickable()
# get_phone_link()
get_phone_data()
driver.quit()
