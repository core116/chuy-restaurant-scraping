"""
This is a web scraper for Chuys Restaurants 
"""

# Importing required modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

current_date = datetime.now().date()

# Setting options for Chrome Webdriver
chrome_options = Options()
# chrome_options.add_argument("--headless=new")
chrome_options.add_argument("−−lang=en-US")
driver = webdriver.Chrome(chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 30) # Sets a wait time for driver before throwing an exception

while True:
    try:
        driver.get("https://order.chuys.com/")
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@data-test-form-field-input="vendor-search-nearby"]')))
        address_input =  driver.find_element(By.XPATH, '//input[@data-test-form-field-input="vendor-search-nearby"]')
        address_input.click()
        address_input.send_keys("Austin")
        order_button = driver.find_element(By.XPATH, '//button[@data-test-vendorsearchform-submit]')
        order_button.click()
        break
    except Exception as e:
        continue

while True:
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@data-test-card-grid]/li[1]/div/div[2]/button')))
        nav_button = driver.find_element(By.XPATH, '//ul[@data-test-card-grid]/li[1]/div/div[2]/button')
        nav_button.click()
        break
    except Exception as e:
        continue

output_array = [['item_id','company_name','item_name','protein_option','price','description','added_date', 'last_modified_date', 'discontinued_date']]

while True:
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//button[@data-test-button="start-group-order"]')))
        sections_list = driver.find_elements(By.XPATH, '//section[@data-test-stickynav-section]')
        for section in sections_list:
            category_name = section.find_element(By.XPATH, './/header/div/h2').text
            sub_category_list = section.find_elements(By.XPATH, './/ul[@data-test-carousel-list]/li')
            for sub_category in sub_category_list:
                sub_category_name = sub_category.find_element(By.XPATH, './/a[@data-test-productcard-name-link]').text
                try:
                    price = sub_category.find_element(By.XPATH, './/p[@data-test-productcard-price]').text
                except:
                    price = ''
                try:
                    des = sub_category.find_element(By.XPATH, './/p[@data-test-productcard-description]').text
                except:
                    des = ''
                item_id = len(output_array)
                output_array.append([item_id, 'Chuys', category_name, sub_category_name, price, des, current_date, current_date, 'none'])

        break
    except Exception as e:
        print(e)
        continue

# Open the file with permissions to write, and specify formatting details
with open('chuys.csv', 'w', newline='', encoding='utf-8') as file:

    # Create a writing object
    writer = csv.writer(file)

    # Write output data to the CSV file
    writer.writerows(output_array)