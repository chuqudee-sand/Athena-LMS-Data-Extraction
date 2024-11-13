import streamlit as st

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

# Add a scrape button when all selections are made
if all(x != "Select Cohort..." and x != "Select Module..." and x != "Select MCQ..." 
       for x in [cohort, module, mcq]):
    if st.button("Scrape Scores"):
        st.info("Scraping functionality will be implemented here")
