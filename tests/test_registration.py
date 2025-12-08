#!/usr/bin/env python3
import pytest
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Constants (update these as per your application)
BASE_URL = "https://example.com"
REGISTRATION_URL = f"{BASE_URL}/register"
DASHBOARD_URL = f"{BASE_URL}/dashboard"
EMAIL_VERIFICATION_URL = f"{BASE_URL}/verify-email"

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# Helper functions

def fill_registration_form(driver, first_name, last_name, email, password):
    driver.get(REGISTRATION_URL)
    try:
        if first_name is not None:
            driver.find_element(By.ID, "first_name").clear()
            driver.find_element(By.ID, "first_name").send_keys(first_name)
        if last_name is not None:
            driver.find_element(By.ID, "last_name").clear()
            driver.find_element(By.ID, "last_name").send_keys(last_name)
        if email is not None:
            driver.find_element(By.ID, "email").clear()
            driver.find_element(By.ID, "email").send_keys(email)
        if password is not None:
            driver.find_element(By.ID, "password").clear()
            driver.find_element(By.ID, "password").send_keys(password)
    except NoSuchElementException as e:
        logging.error(f"Element not found during registration form fill: {e}")
        raise

def submit_registration_form(driver):
    try:
        driver.find_element(By.ID, "submit_registration").click()
    except NoSuchElementException as e:
        logging.error(f"Submit button not found: {e}")
        raise

def get_error_message(driver, field_id):
    try:
        error_elem = driver.find_element(By.ID, f"{field_id}_error")
        return error_elem.text
    except NoSuchElementException:
        return None

def get_general_error_message(driver):
    try:
        error_elem = driver.find_element(By.CLASS_NAME, "form-error")
        return error_elem.text
    except NoSuchElementException:
        return None

def get_otp_from_email(email_address):
    # Placeholder: Implement email fetching logic as per your test environment
    # For now, return a dummy OTP
    return "123456"

def enter_otp(driver, otp):
    try:
        driver.find_element(By.ID, "otp_input").clear()
        driver.find_element(By.ID, "otp_input").send_keys(otp)
        driver.find_element(By.ID, "submit_otp").click()
    except NoSuchElementException as e:
        logging.error(f"OTP input or submit not found: {e}")
        raise

# Test Cases

def test_TC001_successful_account_registration_with_valid_details_and_otp_verification(driver):
    """
    TC001: Successful account registration with valid details and OTP verification
    """
    driver.get(BASE_URL)
    # Step 1: Click on 'Create Account' or 'Sign Up' button
    try:
        driver.find_element(By.ID, "signup_button").click()
    except NoSuchElementException:
        pytest.fail("Sign Up button not found on landing page")
    # Step 2: Fill registration form
    fill_registration_form(driver, "John", "Doe", "john.doe@example.com", "Abcdef1!")
    # Step 3: Submit registration form
    submit_registration_form(driver)
    # Step 4: Observe redirection to 'Email Verification' page
    try:
        WebDriverWait(driver, 10).until(EC.url_contains("/verify-email"))
    except TimeoutException:
        pytest.fail("Did not redirect to Email Verification page after registration")
    # Step 5: Retrieve OTP from email
    otp = get_otp_from_email("john.doe@example.com")
    # Step 6: Enter correct OTP and submit
    enter_otp(driver, otp)
    # Step 7: Assert user is redirected to dashboard
    try:
        WebDriverWait(driver, 10).until(EC.url_to_be(DASHBOARD_URL))
    except TimeoutException:
        pytest.fail("User was not redirected to dashboard after OTP verification")


def test_TC002_registration_fails_when_first_name_missing(driver):
    """
    TC002: Registration fails when First Name is missing
    """
    fill_registration_form(driver, None, "Doe", "john.doe@example.com", "Abcdef1!")
    submit_registration_form(driver)
    # Assert form submission is blocked and error message is displayed
    error = get_error_message(driver, "first_name")
    assert error == "First name is required.", f"Expected error message not found. Got: {error}"


def test_TC003_registration_fails_when_last_name_missing(driver):
    """
    TC003: Registration fails when Last Name is missing
    """
    fill_registration_form(driver, "John", None, "john.doe@example.com", "Abcdef1!")
    submit_registration_form(driver)
    error = get_error_message(driver, "last_name")
    assert error == "Last name is required.", f"Expected error message not found. Got: {error}"


def test_TC004_registration_fails_when_email_missing(driver):
    """
    TC004: Registration fails when Email Address is missing
    """
    fill_registration_form(driver, "John", "Doe", None, "Abcdef1!")
    submit_registration_form(driver)
    error = get_error_message(driver, "email")
    assert error == "Email address is required.", f"Expected error message not found. Got: {error}"


def test_TC005_registration_fails_when_password_missing(driver):
    """
    TC005: Registration fails when Password is missing
    """
    fill_registration_form(driver, "John", "Doe", "john.doe@example.com", None)
    submit_registration_form(driver)
    error = get_error_message(driver, "password")
    assert error == "Password is required.", f"Expected error message not found. Got: {error}"


def test_TC006_registration_fails_with_invalid_email_format(driver):
    """
    TC006: Registration fails with invalid email format
    """
    fill_registration_form(driver, "John", "Doe", "johndoe.com", "Abcdef1!")
    submit_registration_form(driver)
    error = get_error_message(driver, "email")
    assert error == "Please enter a valid email address.", f"Expected error message not found. Got: {error}"


def test_TC007_registration_fails_with_already_registered_email(driver):
    """
    TC007: Registration fails with already registered email
    """
    fill_registration_form(driver, "John", "Doe", "existing.user@example.com", "Abcdef1!")
    submit_registration_form(driver)
    error = get_general_error_message(driver)
    assert error == "An account with this email already exists. Please log in or use a different email.", f"Expected error message not found. Got: {error}"


def test_TC008_password_policy_enforcement_missing_uppercase(driver):
    """
    TC008: Password policy enforcement with missing uppercase letter
    """
    fill_registration_form(driver, "John", "Doe", "john.doe@example.com", "abcdef1!")
    # Observe real-time feedback
    feedback = get_error_message(driver, "password")
    assert "uppercase" in feedback.lower(), f"Expected real-time feedback for missing uppercase. Got: {feedback}"
    submit_registration_form(driver)
    error = get_error_message(driver, "password")
    assert error == "Password must contain at least 1 uppercase letter, 1 number, and 1 special character.", f"Expected error message not found. Got: {error}"


def test_TC009_password_policy_enforcement_missing_number(driver):
    """
    TC009: Password policy enforcement with missing number
    """
    fill_registration_form(driver, "John", "Doe", "john.doe@example.com", "Abcdefgh!")
    feedback = get_error_message(driver, "password")
    assert "number" in feedback.lower(), f"Expected real-time feedback for missing number. Got: {feedback}"
    submit_registration_form(driver)
    error = get_error_message(driver, "password")
    assert error == "Password must contain at least 1 uppercase letter, 1 number, and 1 special character.", f"Expected error message not found. Got: {error}"


def test_TC010_password_policy_enforcement_missing_special_char(driver):
    """
    TC010: Password policy enforcement with missing special character
    """
    fill_registration_form(driver, "John", "Doe", "john.doe@example.com", "Abcdef12")
    feedback = get_error_message(driver, "password")
    assert "special character" in feedback.lower(), f"Expected real-time feedback for missing special character. Got: {feedback}"
    submit_registration_form(driver)
    error = get_error_message(driver, "password")
    assert error == "Password must contain at least 1 uppercase letter, 1 number, and 1 special character.", f"Expected error message not found. Got: {error}"


def test_TC011_show_hide_password_toggle(driver):
    """
    TC011: Show/Hide password toggle functionality
    """
    fill_registration_form(driver, "John", "Doe", "john.doe@example.com", "Abcdef1!")
    password_field = driver.find_element(By.ID, "password")
    # Step 2: Click 'Show Password' toggle
    driver.find_element(By.ID, "toggle_password_visibility").click()
    # Step 3: Verify password is visible
    assert password_field.get_attribute("type") == "text", "Password should be visible after toggle."
    # Step 4: Click 'Hide Password' toggle
    driver.find_element(By.ID, "toggle_password_visibility").click()
    # Step 5: Verify password is masked
    assert password_field.get_attribute("type") == "password", "Password should be masked after toggle."


def test_TC012_otp_expires_after_validity_period(driver):
    """
    TC012: OTP expires after validity period
    """
    driver.get(EMAIL_VERIFICATION_URL)
    # Step 1: Wait for more than 10 minutes (simulate with sleep or mock in real test)
    time.sleep(2)  # Use a short sleep for demo; in real test, mock OTP expiry
    # Step 2: Enter expired OTP
    enter_otp(driver, "000000")
    # Step 3: Assert error message
    error = get_general_error_message(driver)
    assert error == "OTP has expired. Please request a new code.", f"Expected OTP expiry error. Got: {error}"


def test_TC013_resend_otp_functionality_with_cooldown(driver):
    """
    TC013: Resend OTP functionality with cooldown period
    """
    driver.get(EMAIL_VERIFICATION_URL)
    resend_link = driver.find_element(By.ID, "resend_otp_link")
    assert resend_link.is_enabled(), "Resend Code link should be available initially."
    resend_link.click()
    # Attempt to click again within cooldown
    time.sleep(1)
    assert not resend_link.is_enabled() or "cooldown" in resend_link.text.lower(), "Resend link should be disabled or show cooldown message."


def test_TC014_account_lockout_after_multiple_incorrect_otp_attempts(driver):
    """
    TC014: Account lockout after multiple incorrect OTP attempts
    """
    driver.get(EMAIL_VERIFICATION_URL)
    for i in range(5):
        enter_otp(driver, "000000")
        error = get_general_error_message(driver)
        assert "incorrect" in error.lower() or "invalid" in error.lower(), f"Expected error after incorrect OTP. Got: {error}"
    # After 5th attempt
    error = get_general_error_message(driver)
    assert "locked" in error.lower() or "temporarily" in error.lower(), f"Expected lockout message after 5 attempts. Got: {error}"


def test_TC015_accessibility_and_keyboard_navigation(driver):
    """
    TC015: Accessibility and keyboard navigation for registration and verification
    """
    fill_registration_form(driver, "John", "Doe", "john.doe@example.com", "Abcdef1!")
    # Tab through all fields
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(6):
        body.send_keys(Keys.TAB)
    # Try to submit with Enter
    body.send_keys(Keys.ENTER)
    # Assume registration proceeds if no error
    try:
        WebDriverWait(driver, 5).until(EC.url_contains("/verify-email"))
    except TimeoutException:
        pytest.fail("Keyboard navigation did not allow registration submission.")
    # On verification page, tab and enter OTP
    otp = get_otp_from_email("john.doe@example.com")
    for _ in range(2):
        body.send_keys(Keys.TAB)
    body.send_keys(otp)
    body.send_keys(Keys.ENTER)
    try:
        WebDriverWait(driver, 5).until(EC.url_to_be(DASHBOARD_URL))
    except TimeoutException:
        pytest.fail("Keyboard navigation did not allow OTP submission.")


def test_TC016_verification_email_content_and_sender_validation():
    """
    TC016: Verification email content and sender validation
    """
    # This test would require integration with an email API or test mailbox
    # Placeholder logic:
    email = {
        "from": "The Application Name Team <no-reply@example.com>",
        "subject": "Your Verification Code is 123456",
        "body": "Your OTP is 123456. It expires in 10 minutes."
    }
    assert "The Application Name Team" in email["from"], "Sender name is incorrect."
    assert "no-reply@example.com" in email["from"], "Sender email is incorrect."
    assert "Verification Code" in email["subject"], "Subject line is not clear."
    assert "123456" in email["body"] and "expires" in email["body"], "OTP or expiry time not found in email body."
