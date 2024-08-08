import json
import pprint
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By

# Create Chromeoptions instance 
options = webdriver.ChromeOptions() 
# Adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
# Exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
# Turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 

# Setup
city = input("Enter the city and province (in two letters) you want to seach in: ")
province = input("Enter province in two letters: ")
transaction_type = input("Sale or rent: ")
transaction_types = {"sale": 1, "rent": 3}

# Session launch
driver = webdriver.Chrome(options=options)
url = f"https://www.realtor.ca/map#ZoomLevel=10&Center=43.708087%2C-79.376385&LatitudeMax=43.99775&LongitudeMax=-78.75222&LatitudeMin=43.41702&LongitudeMin=-80.00055&CurrentPage=1&Sort=6-D&PGeoIds=g30_dpz89rm7&PropertyTypeGroupID=1&TransactionTypeId={transaction_types[transaction_type.strip().lower()]}&PropertySearchTypeId=0&Currency=CAD&HiddenListingIds=&IncludeHiddenListings=false"
driver.get(url=url)
time.sleep(20)

# City search
soup = BeautifulSoup(driver.page_source, "html.parser")
city_input = driver.find_element(By.XPATH, '//*[@id="txtMapSearchInput"]')
city_input.send_keys(city)
search_button = driver.find_element(By.XPATH, '//*[@id="btnMapSearch"]')
search_button.click()
time.sleep(10)

# Rentals parsing
all_rentals = []
while True: 
    soup = BeautifulSoup(driver.page_source, "html.parser")
    div_container = soup.find_all('div', attrs={"class": "cardCon"})
    for item in div_container:

        additional_info = {}
        info_divs = item.find_all('div', attrs={"class": "smallListingCardIconCon"})
        for info in info_divs:
            additional_info[f"{info.find('div', attrs={"class": "smallListingCardIconText"}).text}"] = info.find('div', attrs={"class": "smallListingCardIconNum"}).text

        price_text = item.find('div', attrs={"class": "smallListingCardPrice"}).text.strip()
        price_text = price_text[re.search(r"\d", price_text).start():]
        if price_text.__contains__("/"):
            if price_text.__contains__(" "):
                price = eval(price_text[price_text.index(" ")+1:price_text.index("/")].replace('$', "").replace(',', ""))
            else: price = eval(price_text[:price_text.index("/")].replace('$', "").replace(',', ""))
        else: price = eval(price_text)

        rental = {
            "price": price,
            "address": item.find('div', attrs={"class": "smallListingCardAddress"}).text,
            "info": additional_info
        }

        if price_text.__contains__("/") :
            pay_frequencey = price_text[price_text.index('/') + 1:]
            rental["pay frequency"] = pay_frequencey
        all_rentals.append(rental)

    next_page_button = driver.find_element(By.XPATH, '//*[@id="SideBarPagination"]/div/a[3]')
    if next_page_button and next_page_button.get_attribute('disabled') == 'true': 
        driver.quit(); 
        break
    else: next_page_button.click(); time.sleep(3)

all_rentals.sort(key=lambda x: x['price'])

try: 
    print("Your best option is: ")
    pprint.pprint(all_rentals[0], indent=4, compact=False)
    json.dump(all_rentals, fp=open('result.txt', 'w'), indent=4)
except IndexError:
    print("No result found")