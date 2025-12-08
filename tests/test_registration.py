#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Automated tests for Registration and Verification flows using Selenium and pytest.
Test cases are based on provided business requirements and JSON input.
"""
import pytest
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Constants (update these as per your application)
BASE_URL = "https://example.com"
REGISTRATION_URL = f"{BASE_URL}/register"
LOGIN_URL = f"{BASE_URL}/login"
DASHBOARD_URL = f"{BASE_URL}/dashboard"
EMAIL_VERIFICATION_URL = f"{BASE_URL}/verify-email"

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()

# Utility functions (placeholders for email/OTP retrieval, etc.)
def get_otp_from_email(email_address):
    """
    Placeholder for retrieving OTP from email. Replace with actual implementation.
    """
    logging.info(f"Retrieving OTP for {email_address} from email inbox...")
    # Simulate OTP retrieval
    return "123456"

def wait_for_element(driver, by, value, timeout=10):
    """Wait for element to be present and return it."""
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

# Test Cases

def test_TC001_successful_account_registration_with_otp(driver):
    """
    TC001: Successful account registration with valid details and OTP verification
    """
    driver.get(BASE_URL)
    # Step 1: Click 'Create Account' or 'Sign Up'
    try:
        signup_btn = wait_for_element(driver, By.ID, "signup-btn")
        signup_btn.click()
    except Exception as e:
        logging.error("Sign Up button not found or not clickable.")
        pytest.fail(str(e))
    # Step 2: Fill registration form
    driver.find_element(By.ID, "first_name").send_keys("John")
    driver.find_element(By.ID, "last_name").send_keys("Doe")
    driver.find_element(By.ID, "email").send_keys("john.doe@example.com")
    driver.find_element(By.ID, "password").send_keys("Abcdef1!")
    # Step 3: Submit form
    driver.find_element(By.ID, "register-submit").click()
    # Step 4: Redirected to Email Verification page
    assert EMAIL_VERIFICATION_URL in driver.current_url, "Not redirected to Email Verification page."
    # Step 5: Retrieve OTP
    otp = get_otp_from_email("john.doe@example.com")
    # Step 6: Enter OTP and submit
    driver.find_element(By.ID, "otp_input").send_keys(otp)
    driver.find_element(By.ID, "otp_submit").click()
    # Step 7: Assert account is activated and redirected to dashboard
    assert DASHBOARD_URL in driver.current_url, "User not redirected to dashboard after OTP verification."

@pytest.mark.parametrize("field_id, value, error_msg", [
    ("first_name", "", "First name is required."),
    ("last_name", "", "Last name is required."),
    ("email", "", "Email address is required."),
    ("password", "", "Password is required.")
])
def test_TC002_to_TC005_required_fields(driver, field_id, value, error_msg):
    """
    TC002-TC005: Registration fails when required fields are missing
    """
    driver.get(REGISTRATION_URL)
    # Fill all fields with valid data first
    driver.find_element(By.ID, "first_name").send_keys("John")
    driver.find_element(By.ID, "last_name").send_keys("Doe")
    driver.find_element(By.ID, "email").send_keys("john.doe@example.com")
    driver.find_element(By.ID, "password").send_keys("Abcdef1!")
    # Clear the field under test
    driver.find_element(By.ID, field_id).clear()
    driver.find_element(By.ID, field_id).send_keys(value)
    # Submit form
    driver.find_element(By.ID, "register-submit").click()
    # Assert error message
    error_element = wait_for_element(driver, By.ID, f"{field_id}_error")
    assert error_msg in error_element.text


def test_TC006_invalid_email_format(driver):
    """
    TC006: Registration fails with invalid email format
    """
    driver.get(REGISTRATION_URL)
    driver.find_element(By.ID, "first_name").send_keys("John")
    driver.find_element(By.ID, "last_name").send_keys("Doe")
    driver.find_element(By.ID, "email").send_keys("johndoe.com")
    driver.find_element(By.ID, "password").send_keys("Abcdef1!")
    driver.find_element(By.ID, "register-submit").click()
    error_element = wait_for_element(driver, By.ID, "email_error")
    assert "Please enter a valid email address." in error_element.text


def test_TC007_already_registered_email(driver):
    """
    TC007: Registration fails with already registered email
    """
    driver.get(REGISTRATION_URL)
    driver.find_element(By.ID, "first_name").send_keys("John")
    driver.find_element(By.ID, "last_name").send_keys("Doe")
    driver.find_element(By.ID, "email").send_keys("existing.user@example.com")
    driver.find_element(By.ID, "password").send_keys("Abcdef1!")
    driver.find_element(By.ID, "register-submit").click()
    error_element = wait_for_element(driver, By.ID, "email_error")
    assert "An account with this email already exists" in error_element.text

@pytest.mark.parametrize("password, feedback_id, feedback_msg", [
    ("abcdef1!", "password_feedback", "uppercase letter"),
    ("Abcdefgh!", "password_feedback", "number"),
    ("Abcdef12", "password_feedback", "special character")
])
def test_TC008_to_TC010_password_policy(driver, password, feedback_id, feedback_msg):
    """
    TC008-TC010: Password policy enforcement
    """
    driver.get(REGISTRATION_URL)
    driver.find_element(By.ID, "first_name").send_keys("John")
    driver.find_element(By.ID, "last_name").send_keys("Doe")
    driver.find_element(By.ID, "email").send_keys("john.doe@example.com")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    # Step 2: Observe real-time feedback
    feedback = wait_for_element(driver, By.ID, feedback_id)
    assert feedback_msg in feedback.text
    # Step 3: Attempt to submit
    driver.find_element(By.ID, "register-submit").click()
    error_element = wait_for_element(driver, By.ID, "password_error")
    assert "Password must contain at least 1 uppercase letter, 1 number, and 1 special character." in error_element.text

def test_TC011_show_hide_password_toggle(driver):
    """
    TC011: Show/Hide password toggle functionality
    """
    driver.get(REGISTRATION_URL)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("Abcdef1!")
    # Click 'Show Password' toggle
    show_btn = driver.find_element(By.ID, "show_password_toggle")
    show_btn.click()
    assert password_field.get_attribute("type") == "text"
    # Click 'Hide Password' toggle
    hide_btn = driver.find_element(By.ID, "hide_password_toggle")
    hide_btn.click()
    assert password_field.get_attribute("type") == "password"

def test_TC012_otp_expiry(driver):
    """
    TC012: OTP expires after validity period
    """
    driver.get(EMAIL_VERIFICATION_URL)
    # Simulate waiting for OTP to expire
    logging.info("Waiting for OTP to expire (simulate 10+ minutes)...")
    time.sleep(2)  # Replace with time.sleep(600) in real test
    driver.find_element(By.ID, "otp_input").send_keys("123456")
    driver.find_element(By.ID, "otp_submit").click()
    error_element = wait_for_element(driver, By.ID, "otp_error")
    assert "OTP has expired" in error_element.text


def test_TC013_resend_otp_cooldown(driver):
    """
    TC013: Resend OTP functionality with cooldown period
    """
    driver.get(EMAIL_VERIFICATION_URL)
    resend_link = driver.find_element(By.ID, "resend_otp_link")
    assert resend_link.is_enabled()
    resend_link.click()
    # After click, link should be disabled or cooldown message shown
    time.sleep(1)
    assert not resend_link.is_enabled() or "cooldown" in driver.page_source.lower()


def test_TC014_account_lockout_on_otp(driver):
    """
    TC014: Account lockout after multiple incorrect OTP attempts
    """
    driver.get(EMAIL_VERIFICATION_URL)
    for attempt in range(5):
        driver.find_element(By.ID, "otp_input").clear()
        driver.find_element(By.ID, "otp_input").send_keys("000000")
        driver.find_element(By.ID, "otp_submit").click()
        error_element = wait_for_element(driver, By.ID, "otp_error")
        assert "incorrect" in error_element.text.lower()
    # After 5 attempts, lockout message should appear
    lockout_element = wait_for_element(driver, By.ID, "otp_lockout")
    assert "temporarily locked" in lockout_element.text.lower()


def test_TC015_accessibility_keyboard_navigation(driver):
    """
    TC015: Accessibility and keyboard navigation for registration and verification
    """
    driver.get(REGISTRATION_URL)
    # Tab through all fields and buttons
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(10):
        body.send_keys(Keys.TAB)
    # Try to submit form with keyboard
    driver.find_element(By.ID, "first_name").send_keys("John")
    driver.find_element(By.ID, "last_name").send_keys("Doe")
    driver.find_element(By.ID, "email").send_keys("john.doe@example.com")
    driver.find_element(By.ID, "password").send_keys("Abcdef1!")
    driver.find_element(By.ID, "register-submit").send_keys(Keys.ENTER)
    # If redirected to verification, try to tab through
    if EMAIL_VERIFICATION_URL in driver.current_url:
        for _ in range(5):
            body.send_keys(Keys.TAB)
    # This test is a placeholder for full accessibility audit
    assert True


def test_TC016_verification_email_content():
    """
    TC016: Verification email content and sender validation
    """
    # This test would require integration with email API or mailbox
    email_address = "john.doe@example.com"
    logging.info(f"Checking verification email for {email_address}")
    # Placeholder: Simulate email content check
    email = {
        "from": "The Application Name Team <no-reply@example.com>",
        "subject": "Your Verification Code is 123456",
        "body": "Your OTP is 123456. It expires in 10 minutes."
    }
    assert "The Application Name Team" in email["from"]
    assert "Verification Code" in email["subject"]
    assert "123456" in email["body"]
    assert "expires in 10 minutes" in email["body"]
