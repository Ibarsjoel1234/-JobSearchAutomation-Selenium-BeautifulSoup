from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def automate_job_search(job_role, location, website_url, sort_option="date", wait_time=20):
    driver = webdriver.Chrome()

    print(f"Opening website: {website_url}")
    driver.get(website_url)

    job_title_search_bar = driver.find_element("name", "q")
    job_title_search_bar.send_keys(job_role)

    location_search_bar = driver.find_element("name", "l")
    location_search_bar.clear()
    location_search_bar.send_keys(location)
    location_search_bar.send_keys(Keys.RETURN)

    try:
        print(f"Waiting for job search results (max {wait_time} seconds)...")
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, "jobsearch-SerpJobCard")))
    except Exception as e:
        print(f"Error waiting for search results: {e}")

    # Sort by the specified option or default to sorting by date
    sort_option_xpath = f"//span[text()='{sort_option.capitalize()}']"
    try:
        sort_button = driver.find_element(By.XPATH, sort_option_xpath)
        sort_button.click()
        print(f"Sorting by {sort_option}...")
    except Exception as e:
        print(f"Error sorting by {sort_option}: {e}")
        # If sorting option is not found, default to sorting by date
        print("Defaulting to sorting by date...")
        try:
            date_sort_button = driver.find_element(By.XPATH, "//span[text()='Date']")
            date_sort_button.click()
        except Exception as e:
            print(f"Error sorting by date: {e}")

    extract_job_titles(driver)

    driver.quit()

def extract_job_titles(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_titles = [title.text for title in soup.select('h2.title a')]
    print("Job Titles:", job_titles)

# Example usage
job_role_input = input("Enter the job role: ")
location_input = input("Enter the location: ")
website_keyword = input("Enter the website keyword (e.g., 'indeed'): ")

# Dictionary mapping keywords to website URLs
website_keyword_mapping = {
    'indeed': 'https://ca.indeed.com/',
    'Indeed': 'https://ca.indeed.com/',
    # Add more mappings as needed
}

# Specify the sorting option ("date" for most recent, "relevance" for relevance, etc.)
sort_option_input = input("Enter the sorting option (default is 'date'): ")

# Use the default value "date" if the user doesn't provide a sorting option
sort_option = sort_option_input if sort_option_input else "date"

# Set the desired wait time (in seconds)
wait_time_input = int(input("Enter the wait time (default is 20 seconds): ") or 20)

# Get the website URL based on the provided keyword
website_url = website_keyword_mapping.get(website_keyword)

if website_url:
    # Combine both functions with increased wait time
    automate_job_search(job_role_input, location_input, website_url, sort_option, wait_time_input)
else:
    print(f"Error: No URL found for the provided keyword '{website_keyword}'")
