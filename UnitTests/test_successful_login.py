import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Test Scenario: TS001 - Successful login with valid credentials
@pytest.fixture(scope="module")
def setup():
    # Setup WebDriver
    driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed and added to PATH
    driver.maximize_window()
    yield driver
    driver.quit()

def test_successful_login(setup):
    driver = setup

    # Step 1: Navigate to the login page
    driver.get("https://example.com/login")

    # Verify the login page is loaded
    assert "Login" in driver.title, "Login page did not load successfully."

    # Step 2: Enter a valid username in the 'Username' field
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))  # Replace 'username' with the actual ID of the username field
    )
    username_field.clear()
    username_field.send_keys("valid_username")  # Replace 'valid_username' with actual test data

    # Step 3: Enter a valid password in the 'Password' field
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))  # Replace 'password' with the actual ID of the password field
    )
    password_field.clear()
    password_field.send_keys("valid_password")  # Replace 'valid_password' with actual test data

    # Step 4: Click the 'Login' button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "loginButton"))  # Replace 'loginButton' with the actual ID of the login button
    )
    login_button.click()

    # Expected Result: The user is redirected to their personalized dashboard
    dashboard_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dashboardHeader"))  # Replace 'dashboardHeader' with the actual ID of an element on the dashboard
    )
    assert dashboard_header.is_displayed(), "Dashboard did not load successfully."
    assert "Dashboard" in driver.title, "Dashboard title is incorrect."

    print("Test Scenario TS001: Successful login with valid credentials - Passed")