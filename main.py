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



def product_url_scrapper(amazon_url, search_string, chrome_driver_path):

    # chrome_driver_path =  r"./chromedriver.exe"
    # if not os.path.exists(chrome_driver_path):
    #     raise FileNotFoundError(f"Chromedriver not found at {chrome_driver_path}")

    # # Check if the file is executable
    # if not os.access(chrome_driver_path, os.X_OK):
    #     raise PermissionError(f"Chromedriver at {chrome_driver_path} is not executable")



    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(
        service=service,)


    driver.get(amazon_url)
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
chrome_driver_path = st.text_input('chrome_driver_path')
search_string = st.text_input('Enter some text')
if st.button('scraping'):
    product_links = product_url_scrapper(amazon_url="https://www.amazon.in/", search_string=search_string, chrome_driver_path)
    data = {"product_links": product_links}
    links_data = pd.DataFrame(data)
    st.dataframe(links_data)
