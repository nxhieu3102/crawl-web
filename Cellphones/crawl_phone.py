from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
LINK = 'https://cellphones.com.vn/mobile.html'

driver_path = 'msedgedriver.exe'
driver = webdriver.Edge(executable_path=driver_path)
driver.get(LINK)
ELEMENT_FILE = "phones_element.txt"
DATA_FILE = "phones_data.csv"

# product__price--show
# box-product-name
# technical-content

time.sleep(3)

# click a tag until it is not clickable
# /html/body/div[1]/div/div/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/img
# /html/body/div[1]/div/div/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/img
# /html/body/div[1]/div/div/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/img IMG XPATH
# /html/body/div[1]/div/div/div[3]/div[2]/div/section/div/div[4]/div[1]/div[3]/div[1]/div[1]/p[1] RATING XPATH


def click_a_tag_until_not_clickable():
    while True:
        try:
            time.sleep(1.5)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            a_tag = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div/div[6]/div[5]/div/div[2]/a")
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
    f = open(ELEMENT_FILE, "w+", encoding="utf-8")
    f.write("\n".join(href_list))


def get_phone_data():
    f = open(ELEMENT_FILE, "r+", encoding="utf-8")
    f_csv = open(DATA_FILE, "w+", encoding="utf-8")
    writer = csv.writer(f_csv)
    writer.writerow(["Name", "Price", "Price_Origin",
                    "ROM", "PIN", "LINK", "IMG", "RATING"])

    href_list = f.readlines()

    for href in href_list:
        driver.get(href)
        time.sleep(1.5)
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
            By.TAG_NAME, 'li') if "Bộ nhớ trong" in element.text]

        pin = [element.text for element in technical.find_elements(
            By.TAG_NAME, 'li') if "Pin" in element.text or "Dung lượng pin" in element.text]

        writer.writerow([name, price, price_origin, rom, pin, href,
                        img, rating])

        print(name, price, rom, pin, price_origin, href, img, rating, )

    f.close()
    f_csv.close()


    # write data above to csv file
# click_a_tag_until_not_clickable()
# get_phone_link()
get_phone_data()
driver.quit()
