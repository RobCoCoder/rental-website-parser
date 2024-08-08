import random
import time
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# 1. data setup
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2719.1708 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6) AppleWebKit/618.5 (KHTML, like Gecko) Version/17.3.22 Safari/618.5",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6296.213 Safari/537.36 OPR/110.0.4495.83",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6300.213 Safari/537.36 OPR/110.0.4478.45",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2126.1580 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15-344",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6342.196 Safari/537.36 OPR/109.0.4814.63",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6287.197 Safari/537.36 OPR/109.0.4961.166",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.170-477",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6) AppleWebKit/617.33.10 (KHTML, like Gecko) Version/17.7.60 Safari/617.33.10",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
]
url = "https://www.realtor.ca/map#ZoomLevel=10&Center=43.708087%2C-79.376385&LatitudeMax=43.99775&LongitudeMax=-78.75222&LatitudeMin=43.41702&LongitudeMin=-80.00055&CurrentPage=45&Sort=6-D&PGeoIds=g30_dpz89rm7&GeoName=Toronto%2C%20ON&PropertyTypeGroupID=1&TransactionTypeId=3&PropertySearchTypeId=0&Currency=CAD&HiddenListingIds=&IncludeHiddenListings=false"
headers = {
    "referer": "https://prerender.io/",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ru,en;q=0.9,fr;q=0.8",
    "cache-control": "max-age=0",
    "cookie": "__AntiXsrfToken=ec74704b2df04cc88f5a79bf685505c1; Language=1; app_mode=1; Currency=CAD; cmsdraft=False; GUID=8a3e6b8e-cf46-4b68-8049-c15d133c0dd8; visid_incap_2269415=INb0Vmk3RxitEcTPjPq5eA78sGYAAAAAQUIPAAAAAABYd5MeRvbzOX2eUFcDqZXe; incap_ses_1849_2269415=UzSkG2J0K3jtvMPSuPeoGRb8sGYAAAAAAo8R5fyVBxbKacZDoY2Cuw==; gig_canary=false; visid_incap_3057435=0uof/JScRESkVmBeC1uSPBf8sGYAAAAAQUIPAAAAAADdyR3SPSyA7OLb+RFzUZ/r; nlbi_3057435=I3ZGSVKutFq4thxOoWGLxgAAAABJXKE7lEPKU55VO320lh+V; incap_ses_1849_3057435=FBRlPc6z6jyT1cPSuPeoGRf8sGYAAAAAkQJtgq4KBLEuZ31FaRe3jw==; gig_bootstrap_3_mrQiIl6ov44s2X3j6NGWVZ9SDDtplqV7WgdcyEpGYnYxl7ygDWPQHqQqtpSiUfko=gigya-pr_ver4; visid_incap_2271082=ozsKJe0aTCq+YEF63ce8Hxn8sGYAAAAAQUIPAAAAAAAMJ8T3q8W1hjgw4zVTn+RZ; nlbi_2271082=2RnIH74mmxYBET2vVPrQ3QAAAAAlQKjM04+REgu1cbdR8P4K; incap_ses_1849_2271082=2Xlaet7iwk2x28PSuPeoGRn8sGYAAAAATAG+vFh0ElsZcNhr4x5JYA==; ll-visitor-id=5864f55d-5f20-47c9-9584-a55c9d930408; TermsOfUseAgreement=2018-06-07; nlbi_2271082_2147483392=sUrFEbvCMX9ftPqNVPrQ3QAAAADgBq4bVh2TUilhruWz4ZYx; gig_canary_ver=16174-3-28714590; reese84=3:Y0Xq5c2PsX5HT+RrzvruZg==:Z7b18aF8OURTkSjAzd15sHvUk+rl7Z8Jf5W0Jj3OULQrwjTQ80rzGMH/FbHkyvtuSfToD1UKcBtUV/KbudhDPMnHZYDCJhPOM491RsuS8MyXe2DddcdnX09qCrZTfC8+HhCtuYZoIJcoa80z+krht+PWjubn0B0v2QhyTl+ropVwHtOXBaa0Tb18kObuR+h4ARkvdHhx4bq0oBCQoSBORqOW6uqGJT+NSofTMKkSvhP5Ew2TINL+qFplrLEfMH20+Y2U8I8Y1oJW9vGw5f2GP0w8LdxYEzS1qcMbz3Gin5XyU/oPM/tzZ/AZxyC091HO2wdM2bb9uCRDRWXKg1IL2fEG5t/RJkY9eCYjJ91rbRR0Coc4KHAgkcU7fCuNAF5+RR9GIaSJTdmGw0UEbUhbVtXIiWFHIGCTHsP7d8sE6fHLE0TVtck4wOg+x843KfOElVhhG0XaaO5UorQqwkVPCQ==:DzLLLj5/5qpGemqLPHZhwiLWOXXDZaD3kKdC8wwc/N0=",
    "dnt": "1",
    "priority": "u=0, i",
    "sec-ch-ua": 'Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    'User-Agent': random.choice(user_agents)
}

# Create Chromeoptions instance 
options = webdriver.ChromeOptions() 

# Adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
 
# Exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
# Turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 

# 2. session launch
driver = webdriver.Chrome(options=options)
i = 1
try:
    url = "https://www.realtor.ca/map#ZoomLevel=10&Center=43.708087%2C-79.376385&LatitudeMax=43.99775&LongitudeMax=-78.75222&LatitudeMin=43.41702&LongitudeMin=-80.00055&Sort=6-D&PGeoIds=g30_dpz89rm7&GeoName=Toronto%2C%20ON&PropertyTypeGroupID=1&TransactionTypeId=3&PropertySearchTypeId=0&Currency=CAD&HiddenListingIds=&IncludeHiddenListings=false"
    driver.get(url=url)
    time.sleep(20)
    i+=1
finally:
    while True: 
        all_rentals = []
        soup = BeautifulSoup(driver.page_source, "html.parser")
        div_container = soup.find_all('div', attrs={"class": "cardCon"})
        for item in div_container:
            additional_info = {}
            info_divs = item.find_all('div', attrs={"class": "smallListingCardIconCon"})
            for info in info_divs:
                additional_info[f"{info.find('div', attrs={"class": "smallListingCardIconText"}).text}"] = info.find('div', attrs={"class": "smallListingCardIconNum"}).text

            price_text = item.find('div', attrs={"class": "smallListingCardPrice"}).text.replace('$', "").replace(',', "")
            rental = {
                "price": eval(price_text[:price_text.index('/')]),
                "address": item.find('div', attrs={"class": "smallListingCardAddress"}).text,
                "info": additional_info
            }
            print(rental["price"], rental["address"], rental["info"])
            all_rentals.append(rental)
        next_page_button = driver.find_element(By.XPATH, '//*[@id="SideBarPagination"]/div/a[3]')
        if next_page_button and next_page_button.get_attribute('disabled') == 'true': 
            driver.quit(); 
            break
        else: next_page_button.click(); time.sleep(3)

all_rentals.sort(key=lambda x: x['price'])
with open("result.txt", "w") as text_file:
    for rental in all_rentals:
        text_file.write("""
price: {0},
address: {1},
info: {2}
\n
        """.format(rental["price"], rental["address"], "{" + "\n".join(rental["info"]) + "\n}"))