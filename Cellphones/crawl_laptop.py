from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
LINK = 'https://cellphones.com.vn/laptop.html'

driver_path = 'msedgedriver.exe'
driver = webdriver.Edge(executable_path=driver_path)
driver.get(LINK)
ELEMENT_FILE = "laptop_element.txt"
DATA_FILE = "laptop_data.csv"
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
    elements = driver.find_elements(By.CLASS_NAME, "product-info")
    href_list = [element.find_elements(By.TAG_NAME, 'a')[
        0].get_attribute('href') for element in elements]
    print(href_list)
    f = open("laptop_element.txt", "w+", encoding="utf-8")
    f.write("\n".join(href_list))


def get_phone_data():
    f = open(ELEMENT_FILE, "r+", encoding="utf-8")
    f_csv = open(DATA_FILE, "w+", encoding="utf-8")
    writer = csv.writer(f_csv)
    writer.writerow(["Name", "Price", "Price_Origin", "CPU", "RAM",
                    "ROM", "CARD màn hình", "size màn hình", "LINK", "IMG", "RATING"])

    href_list = f.readlines()

    for href in href_list:
        driver.get(href)
        time.sleep(2)
        if driver.find_elements(By.CLASS_NAME, "product__price--show") == []:
            continue
        name = driver.find_element(By.CLASS_NAME, "box-product-name").text
        price = driver.find_element(By.CLASS_NAME, "product__price--show").text
        price_origin = driver.find_elements(
            By.CLASS_NAME, "product__price--through")
       
        if price_origin == []:
            price_origin = "None"
        else:
            price_origin = price_origin[0].text
        
        img = driver.find_elements(
            By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/img")

        if img == []:
            img = driver.find_elements(
                By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/div[2]/div/div[3]/img")
        img = img[0].get_attribute('src')

        rating = driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div/section/div/div[4]/div[1]/div[3]/div[1]/div[1]/p[1]").text
        
        button = driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div/section/div/div[4]/div[2]/div[1]/button")
        driver.execute_script("arguments[0].click();", button)

        technical = driver.find_element(
            By.CLASS_NAME, "technical-content-modal")
        rom = [element.text for element in technical.find_elements(
            By.TAG_NAME, 'li') if "Rom" in element.text or "Ổ cứng" in element.text]
        cpu = [element.text for element in technical.find_elements(
            By.TAG_NAME, 'li') if "Loại CPU" in element.text]
        card = [element.text for element in technical.find_elements(
            By.TAG_NAME, 'li') if "Loại card đồ họa" in element.text]
        size = [element.text for element in technical.find_elements(
            By.TAG_NAME, 'li') if "Kích thước màn hình" in element.text]
        ram = [element.text for element in technical.find_elements(
            By.TAG_NAME, 'li') if "Dung lượng RAM" in element.text]
        
        # ["Name", "Price", "Price_Origin", "CPU", "RAM",
                    # "ROM", "CARD màn hình", "size màn hình", "LINK", "IMG", "RATING"]
        writer.writerow([name, price, price_origin, cpu, ram, rom, card, size, href, img, rating])

        print(name, price, price_origin, cpu, ram, rom, card, size, href, img, rating)

    f.close()
    f_csv.close()


    # write data above to csv file
# click_a_tag_until_not_clickable()
# get_phone_link()
get_phone_data()
driver.quit()
