import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime

# Page config
st.set_page_config(
    page_title="MCQ Score Scraper",
    page_icon="📊",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Navigation")

# Cohort filter with associated IDs
cohort_mapping = {
    "2309-FT Group A": 2,
    "2309-FT Group B": 3,
    "2405-FT": 17,
    "2408-FT": 19,
    "2411-FT": 21
}
cohort = st.sidebar.selectbox(
    "Cohort",
    ["Select Cohort..."] + list(cohort_mapping.keys())
)

# Module filter with associated IDs
module_mapping = {
    "Explore 101": 1,
    "Preparing Data": 2,
    "Querying Data": 3,
    "Visualising Data": 4
}
module = st.sidebar.selectbox(
    "Module",
    ["Select Module..."] + list(module_mapping.keys())
)

# MCQ filter with associated IDs
mcq_mapping = {
    "Flowcharts and Pseudocode": 404,
    "Preparing Data: Integrated Project:(Part 1)": 407,
    "Preparing Data: Integrated Project:(Part 2)": 408,
    "Preparing Data: Drawing and Testing Assumptions": 406,
    "Querying Data: Integrated Project:(Part 1)": 450,
    "Querying Data: Integrated Project:(Part 2)": 451,
    "Querying Data: Integrated Project:(Part 3)": 455,
    "Querying Data: Integrated Project:(Part 4)": 456,
    "Visualising Data: Integrated Project:(Part 1)": 471,
    "Visualising Data: Integrated Project:(Part 2)": 472,
    "Visualising Data: Integrated Project:(Part 3)": 473,
    "Visualising Data: Integrated Project:(Part 4)": 474
}
mcq = st.sidebar.selectbox(
    "MCQ (Integrated Project)",
    ["Select MCQ..."] + list(mcq_mapping.keys())
)

# Main content area
st.title("MCQ Score Scraper")

# Display current selections in main area
st.markdown("### Current Selections:")
st.write(f"**Cohort:** {cohort}")
st.write(f"**Module:** {module}")
st.write(f"**MCQ:** {mcq}")

# Function to initialize the WebDriver
def initialize_driver():
    service = Service('chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    return driver

# Function to log in with user-provided credentials
def login(driver, username, password):
    driver.get('https://alx-learn.explore.ai/faculty/login')
    time.sleep(8)
    driver.get('https://alx-learn.explore.ai/faculty/login')
    time.sleep(5)
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
    time.sleep(5)

# Function to extract table data
def extract_data(driver):
    rows = driver.find_elements(By.XPATH, "//table[@class='table']/tbody/tr")
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        data.append([cell.text for cell in cells])
    df = pd.DataFrame(data, columns=["ID", "Name", "Assessment", "Version", "Status", "Time", "Final_Mark", "Practice_Mark", "Link1", "Link2", "Download1", "Download2"])
    return df

# Function to handle pagination
def click_next_button(driver):
    try:
        next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
        next_button.click()
        time.sleep(5)
    except Exception as e:
        st.error(f"Error clicking 'Next' button: {e}")
        return False
    return True

# User input for credentials
st.markdown("### Enter Your Login Credentials")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Button to trigger extraction
if all(x not in ["Select Cohort...", "Select Module...", "Select MCQ..."] for x in [cohort, module, mcq]):
    if st.button("Scrape Scores"):
        if username and password:
            st.info("Starting data extraction process...")

            # Initialize WebDriver and log in
            driver = initialize_driver()
            login(driver, username, password)

            # Navigate to the specific page for data extraction
            driver.get('https://alx-learn.explore.ai/teacher/assessment/mark')
            time.sleep(3)

            # Select dropdown values
            Select(driver.find_element(By.ID, 'programme_id')).select_by_value(str(cohort_mapping[cohort]))
            time.sleep(5)
            Select(driver.find_element(By.ID, 'phase_id')).select_by_value(str(module_mapping[module]))
            time.sleep(5)
            Select(driver.find_element(By.ID, 'sprint_id')).select_by_value(str(mcq_mapping[mcq]))
            time.sleep(5)

            # Initialize list for DataFrames
            dfs = []

            # Progress bar setup
            total_pages = 20
            progress_bar = st.progress(0)

            # Loop to extract data from each page
            for page_number in range(1, total_pages + 1):
                st.write(f"Extracting data from page {page_number}")
                df = extract_data(driver)
                dfs.append(df)
                progress_bar.progress(page_number / total_pages)
                if page_number < total_pages:
                    success = click_next_button(driver)
                    if not success:
                        break

            # Combine extracted data into a single DataFrame and ensure all columns are string types
            final_df = pd.concat(dfs, ignore_index=True).astype(str)

            # Close the driver
            driver.quit()

            # Create a timestamped file name based on cohort, MCQ, and current date/time
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{cohort}_{mcq}_{timestamp}.csv"

            # Convert DataFrame to CSV and create a download button
            csv_data = final_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download data as CSV",
                data=csv_data,
                file_name=file_name,
                mime="text/csv"
            )
        else:
            st.error("Please enter both username and password.")
