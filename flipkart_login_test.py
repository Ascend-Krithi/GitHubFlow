from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Test credentials
VALID_USERNAME = "validuser@example.com"
VALID_PASSWORD = "ValidPassword123"
INVALID_PASSWORD = "WrongPassword!"
UNREGISTERED_USERNAME = "notregistered@example.com"
INACTIVE_USERNAME = "inactiveuser@example.com"
INACTIVE_PASSWORD = "InactivePassword!"

# Flipkart login page URL
FLIPKART_URL = "https://www.flipkart.com"

# Helper function to open login modal
def open_login_modal(driver):
    # Close initial popup if present
    try:
        close_btn = driver.find_element(By.XPATH, "//button[@class='_2KpZ6l _2doB4z']")
        close_btn.click()
    except:
        pass
    # Click on Login link in header
    try:
        login_link = driver.find_element(By.XPATH, "//a[contains(text(),'Login')]")
        login_link.click()
    except:
        pass

# Helper function to perform login
def perform_login(driver, username, password):
    # Enter username
    username_field = driver.find_element(By.XPATH, "//input[@class='_2IX_2- VJZDxU']")
    username_field.clear()
    username_field.send_keys(username)
    # Enter password
    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    password_field.clear()
    password_field.send_keys(password)
    # Click login button
    login_btn = driver.find_element(By.XPATH, "//button[@class='_2KpZ6l _2HKlqd _3AWRsL']")
    login_btn.click()

# Helper function to get error message
def get_error_message(driver):
    time.sleep(2)
    try:
        error_elem = driver.find_element(By.XPATH, "//span[contains(@class, '_2YULOR')]")
        return error_elem.text
    except:
        return None

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # 1. Successful login with valid credentials
    driver.get(FLIPKART_URL)
    open_login_modal(driver)
    perform_login(driver, VALID_USERNAME, VALID_PASSWORD)
    time.sleep(3)
    # Assert user is redirected to dashboard (check for account element)
    try:
        account_elem = driver.find_element(By.XPATH, "//div[contains(text(),'My Account')]")
        assert account_elem.is_displayed(), "User not redirected to account dashboard"
        print("Test 1 Passed: Successful login with valid credentials.")
    except Exception as e:
        print("Test 1 Failed:", e)

    # 2. Login attempt with incorrect password
    driver.get(FLIPKART_URL)
    open_login_modal(driver)
    perform_login(driver, VALID_USERNAME, INVALID_PASSWORD)
    error_msg = get_error_message(driver)
    assert error_msg and "Incorrect password" in error_msg, "Error message for incorrect password not displayed"
    print("Test 2 Passed: Incorrect password error message displayed.")

    # 3. Login attempt with unregistered email/mobile
    driver.get(FLIPKART_URL)
    open_login_modal(driver)
    perform_login(driver, UNREGISTERED_USERNAME, INVALID_PASSWORD)
    error_msg = get_error_message(driver)
    assert error_msg and "Account not found" in error_msg, "Error message for unregistered account not displayed"
    print("Test 3 Passed: Unregistered account error message displayed.")

    # 4. Login attempt with empty username and password fields
    driver.get(FLIPKART_URL)
    open_login_modal(driver)
    perform_login(driver, "", "")
    error_msg = get_error_message(driver)
    assert error_msg and "Please enter your email/mobile number and password" in error_msg, "Error message for empty fields not displayed"
    print("Test 4 Passed: Empty fields error message displayed.")

    # 5. Account lockout after multiple failed login attempts
    driver.get(FLIPKART_URL)
    open_login_modal(driver)
    for i in range(5):
        perform_login(driver, VALID_USERNAME, INVALID_PASSWORD)
        time.sleep(1)
    error_msg = get_error_message(driver)
    assert error_msg and "Your account has been locked due to multiple failed login attempts" in error_msg, "Account lockout message not displayed"
    print("Test 5 Passed: Account lockout message displayed after multiple failed attempts.")

    # 6. Login page UI validation
    driver.get(FLIPKART_URL)
    open_login_modal(driver)
    # Username field
    username_field = driver.find_element(By.XPATH, "//input[@class='_2IX_2- VJZDxU']")
    assert username_field.is_displayed(), "Username field not present"
    # Password field
    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    assert password_field.is_displayed(), "Password field not present"
    # Login button
    login_btn = driver.find_element(By.XPATH, "//button[@class='_2KpZ6l _2HKlqd _3AWRsL']")
    assert login_btn.is_displayed() and login_btn.is_enabled(), "Login button not present or not enabled"
    # Forgot Password link
    forgot_link = driver.find_element(By.XPATH, "//a[contains(text(),'Forgot?')]")
    assert forgot_link.is_displayed(), "Forgot Password link not present"
    print("Test 6 Passed: Login page UI elements validated.")

    # 7. Login attempt with valid credentials but inactive account
    driver.get(FLIPKART_URL)
    open_login_modal(driver)
    perform_login(driver, INACTIVE_USERNAME, INACTIVE_PASSWORD)
    error_msg = get_error_message(driver)
    assert error_msg and "Your account is inactive. Please contact support." in error_msg, "Inactive account error message not displayed"
    print("Test 7 Passed: Inactive account error message displayed.")

except Exception as e:
    print("Test execution failed:", e)
finally:
    # Cleanup
    driver.quit()
