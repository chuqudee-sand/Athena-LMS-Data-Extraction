# Filename: extract_lms_data.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
import pandas as pd

# Create a Service object for the WebDriver
service = Service('chromedriver-win64/chromedriver.exe')

# Initialize WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# Open the LMS webpage
driver.get('https://alx-learn.explore.ai/faculty/login')

# Wait for the page to load (increase time if needed)
time.sleep(3)

# Log into LMS
username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')
username.send_keys('cokereafor@sandtech.com')
password.send_keys('***********')
password.send_keys(Keys.RETURN)

# Wait for the next page to load after login
time.sleep(5)

# Navigate to the desired page or section, e.g., grades or assignments
driver.get('https://alx-learn.explore.ai/teacher/assessment/mark')

# Wait for the page to load (increase time if needed)
time.sleep(3)

# Select options from dropdown menus
dropdown1 = Select(driver.find_element(By.ID, 'programme_id'))
dropdown1.select_by_value('17')

dropdown2 = Select(driver.find_element(By.ID, 'phase_id'))
dropdown2.select_by_value('2')
time.sleep(8)

dropdown3 = Select(driver.find_element(By.ID, 'sprint_id'))
dropdown3.select_by_value('407')
time.sleep(8)

# Optional: Adjust further interaction time if needed
time.sleep(5)

# Initialize a list to store DataFrames
dfs = []

# Function to extract data from the current page
def extract_data():
    rows = driver.find_elements(By.XPATH, "//table[@class='table']/tbody/tr")
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        data.append([cell.text for cell in cells])
    df = pd.DataFrame(data, columns=["ID", "Name", "Assessment", "Version", "Status", "Time", "Final_Mark", "Practice_Mark", "Link1", "Link2", "Download1", "Download2"])
    return df

# Function to click the "Next" button
def click_next_button():
    try:
        next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
        next_button.click()
        time.sleep(5)
    except Exception as e:
        print(f"Error clicking 'Next' button: {e}")
        return False
    return True

# Loop through pages
for page_number in range(1, 17):
    try:
        print(f"Extracting data from page {page_number}...")
        df = extract_data()
        dfs.append(df)
        if page_number < 16:
            success = click_next_button()
            if not success:
                break
    except Exception as e:
        print(f"Error during extraction: {e}")
        break

# Merge all DataFrames into one
final_df = pd.concat(dfs, ignore_index=True)
