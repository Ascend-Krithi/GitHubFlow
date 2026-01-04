import csv
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Path to your CSV file
CSV_PATH = "TestData/code_creator(testing).csv"

# URL of the login page to test
LOGIN_URL = "http://example.com/login"  # <-- CHANGE THIS to your application's login page

# Locators for the login form elements (update as needed)
USERNAME_LOCATOR = (By.ID, "username")  # <-- Update as per your login page
PASSWORD_LOCATOR = (By.ID, "password")  # <-- Update as per your login page
LOGIN_BUTTON_LOCATOR = (By.ID, "loginBtn")  # <-- Update as per your login page
SUCCESS_INDICATOR_LOCATOR = (By.ID, "dashboard")  # <-- Update as per your login page
ERROR_INDICATOR_LOCATOR = (By.ID, "error-message")  # <-- Update as per your login page

def read_test_data_from_csv(csv_path):
    test_data = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_data.append((
                row['username'],
                row['password'],
                row['expected_status']
            ))
    return test_data

# Read test data once for parameterization
test_data = read_test_data_from_csv(CSV_PATH)

@pytest.mark.parametrize("username,password,expected_status", test_data)
def test_login(username, password, expected_status):
    print(f"Test Case: Login attempt")
    print(f"Input: Username='{username}', Password='{password}'")
    print(f"Expected Result: {expected_status}")

    # Set up WebDriver (uses Chrome by default; ensure chromedriver is installed)
    driver = webdriver.Chrome()
    driver.get(LOGIN_URL)
    time.sleep(1)  # Wait for page to load

    # Find and fill username
    user_field = driver.find_element(*USERNAME_LOCATOR)
    user_field.clear()
    user_field.send_keys(username)

    # Find and fill password
    pass_field = driver.find_element(*PASSWORD_LOCATOR)
    pass_field.clear()
    pass_field.send_keys(password)

    # Print fields to verify data retrieval
    print(f"Utilizing Username: '{username}', Password: '{password}' from sheet.")

    # Click login
    driver.find_element(*LOGIN_BUTTON_LOCATOR).click()
    time.sleep(2)  # Wait for login to process

    # Determine actual result
    actual_result = "failure"
    try:
        # If dashboard or success element is present, login succeeded
        if driver.find_element(*SUCCESS_INDICATOR_LOCATOR).is_displayed():
            actual_result = "success"
    except Exception:
        # If error message or login form remains, login failed
        try:
            if driver.find_element(*ERROR_INDICATOR_LOCATOR).is_displayed():
                actual_result = "failure"
        except Exception:
            actual_result = "failure"

    print(f"Actual Result: {actual_result}")

    # Compare with expected
    status = "Pass" if actual_result == expected_status else "Fail"
    print(f"Status: {status}\n")

    # Optionally, log to a file
    with open("login_test_report.txt", "a") as report:
        report.write(
            f"Test Case: Login attempt\n"
            f"Input: Username='{username}', Password='{password}'\n"
            f"Expected Result: {expected_status}\n"
            f"Actual Result: {actual_result}\n"
            f"Status: {status}\n\n"
        )

    driver.quit()
    assert status == "Pass", f"Test failed for user: {username}"

if __name__ == "__main__":
    pytest.main([__file__])
