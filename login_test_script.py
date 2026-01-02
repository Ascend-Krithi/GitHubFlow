from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# Test Data
FLIPKART_LOGIN_URL = "https://www.flipkart.com/account/login"
REGISTERED_EMAIL = "your_registered_email@example.com"  # Replace with a valid Flipkart email
VALID_PASSWORD = "your_valid_password"                  # Replace with the correct password

# Initialize WebDriver (ensure chromedriver is installed and in PATH)
driver = webdriver.Chrome()

try:
    # Step 1: Navigate to the Flipkart login page
    driver.get(FLIPKART_LOGIN_URL)
    time.sleep(2)  # Wait for the page/modal to load

    # Step 2: Enter a registered email address in the email field
    # The email/mobile field can be identified by its placeholder or autocomplete attribute
    email_field = driver.find_element(By.XPATH, "//input[@type='text' and @autocomplete='username']")
    email_field.clear()
    email_field.send_keys(REGISTERED_EMAIL)

    # Step 3: Enter the correct password in the password field
    password_field = driver.find_element(By.XPATH, "//input[@type='password' and @autocomplete='current-password']")
    password_field.clear()
    password_field.send_keys(VALID_PASSWORD)

    # Step 4: Click the 'Login' button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(., 'Login')]")
    login_button.click()

    # Step 5: Validate expected outcome
    # Wait for redirection and check for a user-specific element (e.g., profile icon or account name)
    time.sleep(5)  # Wait for login and dashboard to load

    # Example: Check for the presence of the account/profile icon
    # The account icon typically has the class '_1q-g33' or you can check for the user's name
    try:
        # Replace with a reliable locator for the account dashboard/homepage
        account_icon = driver.find_element(By.XPATH, "//div[contains(@class, '_1q-g33') or contains(text(), 'My Account')]")
        assert account_icon.is_displayed(), "Account dashboard/homepage not displayed after login."
        print("Login successful: User is redirected to account dashboard/homepage.")
    except NoSuchElementException:
        raise AssertionError("Login failed: Account dashboard/homepage not found.")

except (NoSuchElementException, TimeoutException) as e:
    print(f"Test failed due to element not found or timeout: {e}")
except AssertionError as ae:
    print(f"Assertion failed: {ae}")
finally:
    # Cleanup: Close the browser
    driver.quit()
