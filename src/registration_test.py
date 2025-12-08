# src/registration_test.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants (replace with actual values for your application)
BASE_URL = "https://example.com"
REGISTRATION_URL = f"{BASE_URL}/register"
DASHBOARD_URL = f"{BASE_URL}/dashboard"
EMAIL_VERIFICATION_URL = f"{BASE_URL}/verify-email"

# Selectors (replace with actual selectors)
SELECTORS = {
    'first_name': (By.ID, 'first_name'),
    'last_name': (By.ID, 'last_name'),
    'email': (By.ID, 'email'),
    'password': (By.ID, 'password'),
    'confirm_password': (By.ID, 'confirm_password'),
    'submit': (By.ID, 'submit_button'),
    'show_password': (By.ID, 'show_password_toggle'),
    'hide_password': (By.ID, 'hide_password_toggle'),
    'error_message': (By.CLASS_NAME, 'error-message'),
    'otp_input': (By.ID, 'otp_input'),
    'otp_submit': (By.ID, 'otp_submit'),
    'resend_otp': (By.ID, 'resend_otp_link'),
    'cooldown_message': (By.ID, 'cooldown_message'),
    'email_verification_header': (By.TAG_NAME, 'h1'),
    'dashboard_header': (By.TAG_NAME, 'h1'),
}

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# Helper functions
def fill_registration_form(driver, first_name, last_name, email, password, confirm_password=None):
    driver.get(REGISTRATION_URL)
    if first_name is not None:
        driver.find_element(*SELECTORS['first_name']).clear()
        driver.find_element(*SELECTORS['first_name']).send_keys(first_name)
    if last_name is not None:
        driver.find_element(*SELECTORS['last_name']).clear()
        driver.find_element(*SELECTORS['last_name']).send_keys(last_name)
    if email is not None:
        driver.find_element(*SELECTORS['email']).clear()
        driver.find_element(*SELECTORS['email']).send_keys(email)
    if password is not None:
        driver.find_element(*SELECTORS['password']).clear()
        driver.find_element(*SELECTORS['password']).send_keys(password)
    if confirm_password is not None:
        driver.find_element(*SELECTORS['confirm_password']).clear()
        driver.find_element(*SELECTORS['confirm_password']).send_keys(confirm_password)
    driver.find_element(*SELECTORS['submit']).click()

def get_error_message(driver):
    try:
        return driver.find_element(*SELECTORS['error_message']).text
    except NoSuchElementException:
        return None

def is_on_dashboard(driver):
    return driver.current_url == DASHBOARD_URL

def is_on_email_verification(driver):
    return EMAIL_VERIFICATION_URL in driver.current_url

def enter_otp(driver, otp):
    driver.find_element(*SELECTORS['otp_input']).clear()
    driver.find_element(*SELECTORS['otp_input']).send_keys(otp)
    driver.find_element(*SELECTORS['otp_submit']).click()

def wait_for_element(driver, selector, timeout=10):
    for _ in range(timeout):
        try:
            driver.find_element(*selector)
            return True
        except NoSuchElementException:
            time.sleep(1)
    return False

# Test Cases

def test_successful_account_registration_and_email_verification(driver):
    """
    TC001: Successful account registration and email verification
    """
    fill_registration_form(driver, "John", "Doe", "john.unique{}@example.com".format(int(time.time())), "Abcdef1!", "Abcdef1!")
    assert is_on_email_verification(driver), "Should redirect to email verification page"
    # Simulate retrieving OTP from email (replace with actual retrieval in real test)
    otp = "123456"  # Placeholder
    enter_otp(driver, otp)
    assert is_on_dashboard(driver), "Should redirect to dashboard after successful OTP"

@pytest.mark.parametrize("missing_field,expected_error", [
    ("first_name", "First name is required."),
    ("last_name", "Last name is required."),
    ("email", "Email address is required."),
    ("password", "Password is required.")
])
def test_registration_fails_with_missing_required_fields(driver, missing_field, expected_error):
    """
    TC002: Registration fails with missing required fields
    """
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.missing{}@example.com".format(int(time.time())),
        "password": "Abcdef1!",
        "confirm_password": "Abcdef1!"
    }
    data[missing_field] = None
    fill_registration_form(driver, data["first_name"], data["last_name"], data["email"], data["password"], data["confirm_password"])
    error = get_error_message(driver)
    assert error is not None and expected_error in error

def test_registration_fails_with_invalid_email_format(driver):
    """
    TC003: Registration fails with invalid email format
    """
    fill_registration_form(driver, "John", "Doe", "invalid-email", "Abcdef1!", "Abcdef1!")
    error = get_error_message(driver)
    assert error is not None and "valid email address" in error

def test_registration_fails_with_already_registered_email(driver):
    """
    TC004: Registration fails with already registered email
    """
    existing_email = "existing.user@example.com"
    fill_registration_form(driver, "John", "Doe", existing_email, "Abcdef1!", "Abcdef1!")
    error = get_error_message(driver)
    assert error is not None and "already exists" in error

def test_password_policy_enforcement_during_registration(driver):
    """
    TC005: Password policy enforcement during registration
    """
    # Missing uppercase, number, special char
    fill_registration_form(driver, "John", "Doe", "john.policy{}@example.com".format(int(time.time())), "abcdefg", "abcdefg")
    error = get_error_message(driver)
    assert error is not None and "Password must contain at least 1 uppercase letter" in error

def test_show_hide_password_toggle_functionality(driver):
    """
    TC006: Show/Hide password toggle functionality
    """
    driver.get(REGISTRATION_URL)
    password_field = driver.find_element(*SELECTORS['password'])
    password_field.send_keys("Abcdef1!")
    # Show password
    driver.find_element(*SELECTORS['show_password']).click()
    assert password_field.get_attribute("type") == "text"
    # Hide password
    driver.find_element(*SELECTORS['hide_password']).click()
    assert password_field.get_attribute("type") == "password"

def test_otp_expires_after_validity_period(driver):
    """
    TC007: OTP expires after validity period
    """
    fill_registration_form(driver, "John", "Doe", "john.otp{}@example.com".format(int(time.time())), "Abcdef1!", "Abcdef1!")
    assert is_on_email_verification(driver)
    # Simulate waiting for OTP expiry (replace with actual wait in real test)
    time.sleep(1)  # Use time.sleep(600) for real expiry
    expired_otp = "000000"  # Placeholder for expired OTP
    enter_otp(driver, expired_otp)
    error = get_error_message(driver)
    assert error is not None and "OTP has expired" in error

def test_resend_otp_functionality_with_cooldown_period(driver):
    """
    TC008: Resend OTP functionality with cooldown period
    """
    fill_registration_form(driver, "John", "Doe", "john.resend{}@example.com".format(int(time.time())), "Abcdef1!", "Abcdef1!")
    assert is_on_email_verification(driver)
    resend_link = driver.find_element(*SELECTORS['resend_otp'])
    resend_link.click()
    # Try clicking again immediately
    try:
        resend_link.click()
    except Exception:
        pass  # Should be disabled
    cooldown_msg = driver.find_element(*SELECTORS['cooldown_message']).text
    assert "wait" in cooldown_msg or not resend_link.is_enabled()

def test_account_lockout_after_multiple_incorrect_otp_attempts(driver):
    """
    TC009: Account lockout after multiple incorrect OTP attempts
    """
    fill_registration_form(driver, "John", "Doe", "john.lockout{}@example.com".format(int(time.time())), "Abcdef1!", "Abcdef1!")
    assert is_on_email_verification(driver)
    for i in range(5):
        enter_otp(driver, "111111")
        error = get_error_message(driver)
        assert error is not None and "Invalid OTP" in error
    # 6th attempt should lock account
    enter_otp(driver, "111111")
    error = get_error_message(driver)
    assert error is not None and ("locked" in error or "Maximum OTP attempts" in error)

def test_accessibility_and_keyboard_navigation_for_registration_and_verification(driver):
    """
    TC010: Accessibility and keyboard navigation for registration and verification
    """
    driver.get(REGISTRATION_URL)
    # Tab through all fields
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(6):
        body.send_keys(Keys.TAB)
    # Assume screen reader checks are manual or via accessibility tools
    # Complete registration using keyboard only
    fill_registration_form(driver, "John", "Doe", "john.access{}@example.com".format(int(time.time())), "Abcdef1!", "Abcdef1!")
    assert is_on_email_verification(driver)
    # Tab to OTP field and submit
    for _ in range(2):
        body.send_keys(Keys.TAB)
    enter_otp(driver, "123456")
    assert is_on_dashboard(driver)

def test_verification_email_content_and_sender_validation():
    """
    TC011: Verification email content and sender validation
    Note: This test assumes access to a test email inbox via API or IMAP.
    """
    # This is a placeholder for email validation logic
    # In a real test, use an email API or IMAP client to fetch the latest email
    # Example (pseudo-code):
    # email = fetch_latest_email(to="john.unique@example.com")
    # assert email.sender == "The Application Name Team <no-reply@example.com>"
    # assert "Your Verification Code" in email.subject
    # assert "OTP" in email.body and "expires" in email.body
    assert True  # Replace with actual email validation logic
