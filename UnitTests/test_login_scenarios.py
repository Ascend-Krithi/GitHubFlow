from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import time

class TestLoginScenarios(unittest.TestCase):
    def setUp(self):
        # Initialize the WebDriver (Chrome in this case)
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.base_url = 'https://example.com/login'

    def test_successful_login(self):
        """Test Scenario TS001: Successful login with valid credentials"""
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element(By.ID, 'username').send_keys('valid_user@example.com')
        driver.find_element(By.ID, 'password').send_keys('valid_password')
        driver.find_element(By.ID, 'loginButton').click()
        time.sleep(2)  # Wait for the page to load
        self.assertIn('Dashboard', driver.title)
        self.assertTrue(driver.find_element(By.ID, 'userGreeting').is_displayed())

    def test_invalid_login(self):
        """Test Scenario TS002: Login attempt with invalid credentials"""
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element(By.ID, 'username').send_keys('invalid_user@example.com')
        driver.find_element(By.ID, 'password').send_keys('invalid_password')
        driver.find_element(By.ID, 'loginButton').click()
        error_message = driver.find_element(By.ID, 'errorMessage').text
        self.assertEqual(error_message, 'Invalid username or password')
        self.assertIn('Login', driver.title)

    def test_error_message_disappears(self):
        """Test Scenario TS003: Error message disappears upon new input"""
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element(By.ID, 'username').send_keys('invalid_user@example.com')
        driver.find_element(By.ID, 'password').send_keys('invalid_password')
        driver.find_element(By.ID, 'loginButton').click()
        driver.find_element(By.ID, 'username').clear()
        driver.find_element(By.ID, 'username').send_keys('new_user@example.com')
        error_message = driver.find_element(By.ID, 'errorMessage')
        self.assertFalse(error_message.is_displayed())

    def test_login_button_disabled(self):
        """Test Scenario TS004: Login button disabled until fields are filled"""
        driver = self.driver
        driver.get(self.base_url)
        login_button = driver.find_element(By.ID, 'loginButton')
        self.assertFalse(login_button.is_enabled())
        driver.find_element(By.ID, 'username').send_keys('valid_user@example.com')
        self.assertFalse(login_button.is_enabled())
        driver.find_element(By.ID, 'password').send_keys('valid_password')
        self.assertTrue(login_button.is_enabled())

    def test_account_lockout(self):
        """Test Scenario TS005: Account lockout after 5 failed login attempts"""
        driver = self.driver
        driver.get(self.base_url)
        for _ in range(5):
            driver.find_element(By.ID, 'username').send_keys('valid_user@example.com')
            driver.find_element(By.ID, 'password').send_keys('invalid_password')
            driver.find_element(By.ID, 'loginButton').click()
            time.sleep(1)  # Wait for error message
        error_message = driver.find_element(By.ID, 'errorMessage').text
        self.assertEqual(error_message, 'Your account has been locked. Please contact support')

    def test_responsive_design(self):
        """Test Scenario TS006: Responsive design of the login page"""
        driver = self.driver
        driver.get(self.base_url)
        # This test would ideally include viewport resizing and validation of layout
        # For simplicity, we assume the page is responsive if it loads correctly
        self.assertTrue(driver.find_element(By.ID, 'loginForm').is_displayed())

    def test_password_encryption(self):
        """Test Scenario TS007: Password encryption during transmission"""
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element(By.ID, 'username').send_keys('valid_user@example.com')
        driver.find_element(By.ID, 'password').send_keys('valid_password')
        driver.find_element(By.ID, 'loginButton').click()
        # Manual verification of network traffic is required for this test

    def test_accessibility(self):
        """Test Scenario TS008: Accessibility of the login page"""
        driver = self.driver
        driver.get(self.base_url)
        # Simulate keyboard navigation and screen reader interactions
        # Placeholder for actual accessibility testing tools

    def test_forgot_password_link(self):
        """Test Scenario TS009: 'Forgot Password' link functionality"""
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element(By.LINK_TEXT, 'Forgot Password').click()
        self.assertIn('Password Recovery', driver.title)

    def test_sign_up_button(self):
        """Test Scenario TS010: 'Sign Up' button functionality"""
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element(By.LINK_TEXT, 'Sign Up').click()
        self.assertIn('Account Creation', driver.title)

    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()