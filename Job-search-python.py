from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def automate_job_search(job_role, location, website_url, sort_option="date", wait_time=20):
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    # Open the website
    driver.get(website_url)

    # Find the search bar for job title
    job_title_search_bar = driver.find_element("name", "q")

    # Type the job title you want to search for
    job_title_search_bar.send_keys(job_role)

    # Find the location search bar
    location_search_bar = driver.find_element("name", "l")

    # Clear the previous location if any
    location_search_bar.clear()

    # Type the new desired location
    location_search_bar.send_keys(location)

    # Press Enter to perform the search
    location_search_bar.send_keys(Keys.RETURN)

    # Wait for the search results to load
    try:
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, "jobsearch-SerpJobCard")))
    except Exception as e:
        print(f"Error waiting for search results: {e}")

    # Sort by the specified option (default is "date" for most recent)
    if sort_option == "date":
        sort_button = driver.find_element(By.XPATH, "//span[text()='Date']")
        sort_button.click()

    # Optional: You can perform additional actions here after sorting

    # Extract and print job titles
    extract_job_titles(driver)

    # Close the browser window
    driver.quit()

def extract_job_titles(driver):
    # Extract and print job titles
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
