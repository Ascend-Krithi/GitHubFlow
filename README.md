# Selenium Pytest Registration Automation

## Overview
This repository contains an automated test suite for the user registration and email verification flow using Python Selenium and the pytest framework. The tests cover positive and negative scenarios, including field validation, password policy enforcement, OTP verification, resend/cooldown logic, account lockout, and accessibility.

## Installation
1. Clone the repository:
   ```
   git clone <repository_url>
   cd selenium-pytest-registration-automation
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
- Ensure you have ChromeDriver installed and available in your PATH.
- Update the `BASE_URL` and selectors in `src/registration_test.py` as needed for your application.
- Run all tests:
  ```
  pytest src/
  ```
- To run a specific test:
  ```
  pytest src/registration_test.py::test_successful_account_registration_and_email_verification
  ```

## Prerequisites
- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (matching your Chrome version)
- Access to the application under test
- (Optional) Test email inbox for email/OTP validation

## Directory Structure
- `src/` - Source code for test scripts
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Notes
- Update selectors and URLs in the script to match your application's implementation.
- Some tests (e.g., email content validation) require integration with an email API or test inbox.
- All tests are designed to be run independently and are idempotent.
