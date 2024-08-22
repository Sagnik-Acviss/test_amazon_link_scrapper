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
# options.add_argument("--headless")



def product_url_scrapper(amazon_url, search_string):
    print("check")

    driver = get_driver()
     

    driver.get(amazon_url)
    time.sleep(200)
    driver.find_element(By.XPATH, "//input[@id='twotabsearchtextbox']").send_keys(search_string)

    driver.find_element(By.XPATH, "//input[@id='nav-search-submit-button']").click()
    product_links = []
    # Wait for the results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-component-type="s-search-result"]'))
    )

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        product_elements = driver.find_elements(By.XPATH,
                                                '//div[@data-component-type="s-search-result"]//h2/a')
        for product in product_elements:
            link = product.get_attribute('href')
            if link not in product_links:
                product_links.append(link)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "s-pagination-next")]'))
            )
            next_button.click()
            WebDriverWait(driver, 10).until(
                EC.staleness_of(next_button)  # Wait until the button is stale
            )
        except:
            print("No more pages to scrape.")
            break


    driver.quit()
    return product_links



#
#
# data = {"product_links": product_links}
# links_data = pd.DataFrame(data)
# print(links_data.head())


st.markdown('Get Urls of product from AMAZON')

search_string = st.text_input('Enter some text')
if st.button('scraping'):
    product_links = product_url_scrapper(amazon_url="https://www.amazon.in/", search_string=search_string)
    data = {"product_links": product_links}
    links_data = pd.DataFrame(data)
    st.dataframe(links_data)
