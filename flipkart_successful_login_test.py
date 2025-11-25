from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Replace these with valid Flipkart credentials for testing
VALID_EMAIL_OR_PHONE = "your_registered_email_or_phone"
VALID_PASSWORD = "your_correct_password"

# Initialize WebDriver (ensure chromedriver is in PATH or specify executable_path)
driver = webdriver.Chrome()

try:
    # Step 1: Navigate to the Flipkart login page
    driver.get("https://www.flipkart.com/account/login")
    driver.maximize_window()

    # Wait for the login form to be present
    wait = WebDriverWait(driver, 10)
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='_2IX_2- VJZDxU']")))
    password_field = driver.find_element(By.XPATH, "//input[@type='password']")

    # Step 2: Enter a valid registered email/phone and correct password
    email_field.clear()
    email_field.send_keys(VALID_EMAIL_OR_PHONE)
    password_field.clear()
    password_field.send_keys(VALID_PASSWORD)

    # Step 3: Click on the 'Login' button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(., 'Login')]")
    login_button.click()

    # Step 4: Validate expected outcome
    # Wait for redirection to dashboard/homepage (e.g., check for user profile icon)
    # The user icon usually has the class '_1_4BHq' or similar, but this may change. Adjust as needed.
    # We'll wait for the presence of the account menu or a known element on the logged-in homepage.
    account_icon = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'exehdJ')]")
    ))

    # Assert that the account icon is displayed, indicating successful login
    assert account_icon.is_displayed(), "Login failed: Account dashboard not displayed."

    print("Test Passed: User successfully logged in and redirected to dashboard/homepage.")

except Exception as e:
    print(f"Test Failed: {e}")

finally:
    # Cleanup: Close the browser
    time.sleep(2)
    driver.quit()
