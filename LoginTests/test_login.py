import csv
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Path to the CSV file containing test data
CSV_FILE_PATH = 'LoginTests/test_data.csv'

# Function to read test data from CSV
def read_test_data_from_csv(file_path):
    test_data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Print username and password to verify data retrieval
            print(f"Retrieving from sheet - Username: '{row['username']}', Password: '{row['password']}'")
            test_data.append((row['username'], row['password'], row['expected_status']))
    return test_data

# Load test data
test_cases = read_test_data_from_csv(CSV_FILE_PATH)

@pytest.mark.parametrize("username,password,expected_status", test_cases)
def test_login_functionality(username, password, expected_status):
    # Initialize WebDriver (Chrome in this example)
    driver = webdriver.Chrome()  # Ensure chromedriver is installed and in PATH
    driver.get("http://example.com/login")  # Replace with actual login page URL

    # Locate input fields and login button (replace with actual locators)
    username_field = driver.find_element(By.ID, "username")  # Replace with actual ID
    password_field = driver.find_element(By.ID, "password")  # Replace with actual ID
    login_button = driver.find_element(By.ID, "loginBtn")    # Replace with actual ID

    # Clear fields and enter credentials
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)
    login_button.click()

    time.sleep(2)  # Wait for page to load (use explicit waits in production)

    # Validation logic (customize based on application)
    actual_result = "failure"
    try:
        # Example: Check for successful login by presence of logout button or dashboard
        driver.find_element(By.ID, "logoutBtn")  # Replace with actual locator
        actual_result = "success"
    except:
        # Example: Check for error message
        try:
            error_msg = driver.find_element(By.ID, "errorMsg")  # Replace with actual locator
            actual_result = "failure"
        except:
            actual_result = "failure"

    # Print result in required format
    print(f"Test Case: {'Valid username and password' if expected_status == 'success' else 'Invalid/Empty credentials'}")
    print(f"Input: Username='{username}', Password='{password}'")
    print(f"Expected Result: {expected_status}")
    print(f"Actual Result: {actual_result}")
    print(f"Status: {'Pass' if actual_result == expected_status else 'Fail'}\n")

    # Optionally, log results to a file
    with open('login_test_report.txt', 'a') as report:
        report.write(
            f"Test Case: {'Valid username and password' if expected_status == 'success' else 'Invalid/Empty credentials'}\n"
            f"Input: Username='{username}', Password='{password}'\n"
            f"Expected Result: {expected_status}\n"
            f"Actual Result: {actual_result}\n"
            f"Status: {'Pass' if actual_result == expected_status else 'Fail'}\n\n"
        )

    driver.quit()

if __name__ == "__main__":
    # Run pytest programmatically
    pytest.main([__file__])
