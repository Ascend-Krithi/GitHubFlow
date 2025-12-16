"""
Automated Login Test Script using Selenium, Pytest, and Openpyxl

- Reads test data from Excel (username, password, expected_status)
- Parameterizes test cases with pytest
- Prints test data for verification
- Saves results to a log file
- Includes sample test cases for valid, invalid, and empty credentials
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import openpyxl
import time
import os

# Path to the Excel file containing test data
EXCEL_FILE = 'login_test_data.xlsx'
LOG_FILE = 'login_test_results.log'
LOGIN_URL = 'https://example.com/login'  # Replace with the actual login URL

# Locators for the login page elements (update as per your application)
USERNAME_FIELD = 'username'  # e.g., 'id' or 'name' attribute
PASSWORD_FIELD = 'password'
LOGIN_BUTTON = 'loginBtn'
SUCCESS_INDICATOR = 'dashboard'  # e.g., id or text present after successful login
ERROR_INDICATOR = 'error-message'  # e.g., id or class for error message

# Read test data from Excel
def read_test_data(excel_file):
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active
    test_cases = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        username, password, expected_status = row
        test_cases.append((username, password, expected_status))
    return test_cases

# Pytest parameterization
test_data = read_test_data(EXCEL_FILE)

def pytest_generate_tests(metafunc):
    if 'login_data' in metafunc.fixturenames:
        metafunc.parametrize('login_data', test_data)

# Utility to log results
def log_result(log_file, line):
    with open(log_file, 'a') as f:
        f.write(line + '\n')

@pytest.fixture(scope='session', autouse=True)
def setup_log():
    # Clear log file at start
    with open(LOG_FILE, 'w') as f:
        f.write('Test Case,Input,Expected Result,Actual Result,Status\n')

@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# Main test function
def test_login(driver, login_data):
    username, password, expected_status = login_data
    print(f"Testing with Username: '{username}', Password: '{password}'")
    input_str = f"Username: {username}, Password: {password}"
    actual_result = ''
    status = ''
    try:
        driver.get(LOGIN_URL)
        # Locate fields and perform login
        driver.find_element(By.NAME, USERNAME_FIELD).clear()
        driver.find_element(By.NAME, USERNAME_FIELD).send_keys(username if username is not None else '')
        driver.find_element(By.NAME, PASSWORD_FIELD).clear()
        driver.find_element(By.NAME, PASSWORD_FIELD).send_keys(password if password is not None else '')
        driver.find_element(By.ID, LOGIN_BUTTON).click()
        time.sleep(2)  # Wait for page to load
        # Validation
        if expected_status.lower() == 'success':
            # Check for element indicating successful login
            if SUCCESS_INDICATOR in driver.page_source or driver.find_elements(By.ID, SUCCESS_INDICATOR):
                actual_result = 'success'
                status = 'PASS'
            else:
                actual_result = 'failure'
                status = 'FAIL'
        else:
            # Check for error message
            if ERROR_INDICATOR in driver.page_source or driver.find_elements(By.ID, ERROR_INDICATOR):
                actual_result = 'failure'
                status = 'PASS'
            else:
                actual_result = 'success'
                status = 'FAIL'
    except Exception as e:
        actual_result = f'Error: {str(e)}'
        status = 'ERROR'
    # Output results
    output_line = f"Test Case, {input_str}, {expected_status}, {actual_result}, {status}"
    print(output_line)
    log_result(LOG_FILE, output_line)
    assert status == 'PASS', f"Expected {expected_status}, got {actual_result}"

if __name__ == '__main__':
    # For direct run, invoke pytest
    import sys
    sys.exit(pytest.main([__file__]))
