# Modify the content of `mvp.py` to include functions from `extract_mcq_data.py`
# and handle data extraction on button click in the Streamlit app.

import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

# Page config
st.set_page_config(
    page_title="MCQ Score Scraper",
    page_icon="📊",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Navigation")

# Navigation controls using dropdowns
cohort = st.sidebar.selectbox(
    "Cohort",
    ["Select Cohort...", "Cohort 1", "Cohort 2", "Cohort 3"]  # Replace with actual cohorts
)

module = st.sidebar.selectbox(
    "Module",
    ["Select Module...", "Explore 101", "Data visualization", "SQL"]  # Replace with actual modules
)

mcq = st.sidebar.selectbox(
    "MCQ (Integrated Project)",
    ["Select MCQ...", "IP Week 1", "IP Week 2", "IP Week 3"]  # Replace with actual MCQs
)

# Main content area
st.title("MCQ Score Scraper")

# Display current selections in main area
st.markdown("### Current Selections:")
st.write(f"**Cohort:** {cohort}")
st.write(f"**Module:** {module}")
st.write(f"**MCQ:** {mcq}")

# Functions for data extraction

def initialize_driver():
    # Create a Service object for the WebDriver
    service = Service('chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    return driver

def login(driver, username, password):
    driver.get('https://alx-learn.explore.ai/faculty/login')
    time.sleep(5)
    driver.get('https://alx-learn.explore.ai/faculty/login')
    time.sleep(3)
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
    time.sleep(5)

def extract_data(driver):
    rows = driver.find_elements(By.XPATH, "//table[@class='table']/tbody/tr")
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        data.append([cell.text for cell in cells])
    df = pd.DataFrame(data, columns=["ID", "Name", "Assessment", "Version", "Status", "Time", "Final_Mark", "Practice_Mark", "Link1", "Link2", "Download1", "Download2"])
    return df

def click_next_button(driver):
    try:
        next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
        next_button.click()
        time.sleep(5)
    except Exception as e:
        st.error(f"Error clicking 'Next' button: {e}")
        return False
    return True

# Button to trigger extraction
if all(x != "Select Cohort..." and x != "Select Module..." and x != "Select MCQ..." for x in [cohort, module, mcq]):
    if st.button("Scrape Scores"):
        st.info("Starting data extraction process...")
        
        # Initialize WebDriver and log in (use your credentials or securely handle them)
        driver = initialize_driver()
        login(driver, "cokereafor@sandtech.com", "*********")  # Masked password for security
        
        # Navigate to the specific page for data extraction
        driver.get('https://alx-learn.explore.ai/teacher/assessment/mark')
        time.sleep(3)
        
        # Select dropdown values
        Select(driver.find_element(By.ID, 'programme_id')).select_by_value('17')
        time.sleep(5)
        Select(driver.find_element(By.ID, 'phase_id')).select_by_value('2')
        time.sleep(5)
        Select(driver.find_element(By.ID, 'sprint_id')).select_by_value('407')
        time.sleep(5)
        
        # Initialize list for DataFrames
        dfs = []
        
        # Loop to extract data from each page
        for page_number in range(1, 17):
            st.write(f"Extracting data from page {page_number}...")
            df = extract_data(driver)
            dfs.append(df)
            if page_number < 16:
                success = click_next_button(driver)
                if not success:
                    break

        # Combine extracted data into a single DataFrame
        final_df = pd.concat(dfs, ignore_index=True)

        # Convert all columns to string to ensure compatibility with Streamlit
        final_df = final_df.astype(str)

        # Display the DataFrame in Streamlit
        st.dataframe(final_df)

        # Close the driver
        driver.quit()
        
