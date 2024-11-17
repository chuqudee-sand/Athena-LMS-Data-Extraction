
# Athena LMS MCQ Results Extractor

This project is a Python script that uses Selenium and BeautifulSoup to extract students' MCQ results from the Athena LMS platform. The extracted data includes student IDs, names, assessments, status, final marks, and other relevant information. The script navigates through multiple pages to gather all the data, saving it to a combined DataFrame for easy analysis.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Data Fields](#data-fields)
- [Contributing](#contributing)

## Features

- Automates login to the Athena LMS platform.
- Navigates through multiple pages to extract MCQ results.
- Saves extracted data into a pandas DataFrame.
- Configurable to extract data from different assessment sections using dropdown selections.

## Requirements

- Python 3.8 or later
- [Selenium](https://pypi.org/project/selenium/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [Pandas](https://pypi.org/project/pandas/)
- Chrome WebDriver (compatible with your Chrome version)

## Setup

1. **Install the required packages**:
   ```bash
   pip install selenium beautifulsoup4 pandas
   ```
2. **Download Chrome WebDriver**:
   - [ChromeDriver](https://sites.google.com/chromium.org/driver/) should match your Chrome browser version. Place the `chromedriver.exe` file in a known path (e.g., `chromedriver-win64/chromedriver.exe`).
   - You can download the chrome driver [here](https://drive.google.com/file/d/1XSIN3yk7wBvxJpByJkGUeyuc7gh0IeJe/view?usp=sharing) if your chrome browser version is 129.0 and above

3. **Configure LMS Login Credentials**:
   - Open the script and replace the placeholders with your Athena LMS username and password:
     ```python
     username.send_keys('your_username')
     password.send_keys('your_password')
     ```

## Usage

1. Run the script:
   ```bash
   python lms_extractor.py
   ```
2. The script will log in, navigate to the MCQ results section, and select the appropriate filters using dropdown menus.
3. Extracted data will be saved to a pandas DataFrame, which can be exported for further analysis.

## Data Fields

The extracted data contains the following columns:

- `ID`: Student ID
- `Name`: Student name
- `Assessment`: Assessment title
- `Version`: Version of the assessment
- `Status`: Completion status
- `Time`: Time taken
- `Final_Mark`: Final mark achieved
- `Practice_Mark`: Practice mark
- `Link1`, `Link2`: Links for further reference
- `Download1`, `Download2`: Downloadable content links

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

