import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
#from seleniumwire import webdriver
from seleniumwire import webdriver
import time
import urllib
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from seleniumwire import webdriver
import time
import urllib
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import streamlit as st
import requests
import os

# from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

@st.cache_resource
def get_driver():
    return webdriver.Chrome(
        service=Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
        options=options,
    )

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("--disable-gpu")  # Applicable for non-GPU environments
options.add_argument("--disable-software-rasterizer")  # Avoid using the GPU entirely
options.add_argument("--remote-debugging-port=9222")  # Port to avoid potential conflicts

def scrape_amazon_reviews(driver,product_url):
    driver.get(product_url)

    # Optional: Wait for reviews to load (could use WebDriverWait for better control)
    driver.implicitly_wait(10)

    # Get review elements
    review_elements = driver.find_elements(By.CSS_SELECTOR, ".a-section.review")

    review_data = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    review_elements1 = soup.find_all('span', {'data-hook': 'review-body'})


    for review in range(len(review_elements)):
        try:
            reviewer_name = review_elements[review].find_element(By.CSS_SELECTOR, ".a-profile-name").text
            review_title = review_elements[review].find_element(By.CSS_SELECTOR, ".review-title-content").text
            review_date = review_elements[review].find_element(By.CSS_SELECTOR, ".review-date").text
            rating = review_elements[review].find_element(By.CSS_SELECTOR, ".a-icon-alt").get_attribute('innerText')

            comment = review_elements1[review].get_text(strip=True)
            #time.sleep(5)
            review_data.append({
                "reviewer_name": reviewer_name,
                "review_title": review_title,
                "review_date": review_date,
                "rating": rating,
                "comment": comment
            })
            print(review_data)
        except Exception as e:
            print(f"Error extracting data: {e}")

    return review_data

g = pd.DataFrame({
                "reviewer_name": [],
                "review_title": [],
                "review_date": [],
                "rating": [],
                "comment": []
            })
def details_scrapper(dataframe, country_code):
    global g

    count = 1
    
    g = pd.DataFrame({
        "reviewer_name": [],
        "review_title": [],
        "review_date": [],
        "rating": [],
        "comment": []
    })
    

    print(dataframe)
    for url in [dataframe]:
        try:
            print(url)
            print(count,"  ", url)
            driver = get_driver()
            driver.get(url=url)

           #  wait = WebDriverWait(driver, 5)  # 10 seconds timeout
            time.sleep(5)
            #driver.find_element(By.XPATH,"//body/div[@id='a-page']/div[@id='dp']/div[@id='dp-container']/div[@id='customer-reviews_feature_div']/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/ul[1]/li[1]/span[1]/a[1]").click()
            # above 5 start click

            print("new : ",driver.current_url)
            s=driver.current_url.split("/")


            print(s)

            for fe in ['five_star','four_star','three_star','two_star','one_star']:
                i = 1
                while True:

                    driver.get("https://www.amazon.in/product-reviews/"+s[5]+rf"/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&filterByStar="+fe+rf"&pageNumber={i}&reviewerType=all_reviews")
                    time.sleep(5)

                    print("https://www.amazon.in/product-reviews/"+s[5]+rf"/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&filterByStar="+fe+rf"&pageNumber={i}&reviewerType=all_reviews")
                    try:
                        if i>=1:
                            span = driver.find_element(By.XPATH, "//span[@class='a-size-medium']").text
                            if span=="Sorry, no reviews match your current selections.":
                                break
                            print(span)
                    except:
                        pass
                    x = scrape_amazon_reviews(driver, driver.current_url)
                    x=pd.DataFrame(x)
                    g = pd.concat([g, x], axis=0)
                    i+=1

            #time.sleep(3000)
            driver.find_element(By.XPATH,"//tbody/tr[2]/td[2]/a[1]").click()
            print(driver.current_url)

            print("----------------------")
        except:
            continue

    driver.quit()
    return g




final = pd.DataFrame({
    "links": [],
    "reviewer_name": [],
    "review_title": [],
    "review_date": [],
    "rating": [],
    "comment": []
})



# url = "https://www.amazon.in/Samsung-EcobubbleTM-Automatic-WA80BG4582BDTL-technology/dp/B0BGL59LZP/ref=sr_1_292?dib=eyJ2IjoiMSJ9.n6ZRFlC2BEMEHQrAiIekZj4DAp8QyikZ98m-IGt871CI3MGTm1rPtpMw94V1Hpn9MxOavqFBxDITBukb4iOVXMnyv7Bg7gODF49dWZ__x8AAy9fAVQYFFKR5aN5QCvsAlQfI183KdbRGhUV3XxPiad6n7CsQOBqyWg4ZBObZGtE.B8Hj8efbS_BusKWhHK0_V4SBk6k6WOPI6N4zEyyqGWo&dib_tag=se&keywords=washing+machine&qid=1724330332&sr=8-292"


st.markdown('Get user comments for AMAZON')
url = st.text_input('Enter URL ')
if st.button('scraping'):
    x = details_scrapper(dataframe=url, country_code="IN")
    x['links'] = [url] * len(x['rating'])
    # x.to_csv(rf"amazon_product_{z}.csv",index=False)
    final = pd.concat([final, x], axis=0)
    # final.to_csv(rf"amazon_product_final.csv", index=False)
    st.dataframe(final)
