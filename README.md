# Automation Test Scripts

This repository contains automation test scripts for login functionality using Selenium and pytest, with parameterized test data from a CSV file.

## Structure
- `LoginTests/test_login.py`: Main test script for login automation.
- `LoginTests/test_data.csv`: Test data for login scenarios (username, password, expected result).

## Usage
1. Ensure `chromedriver` is installed and available in your system PATH.
2. Update the URL and element locators in `test_login.py` to match your application.
3. Run the tests using pytest:
   ```bash
   pytest LoginTests/test_login.py
   ```

## Test Data Format
The CSV file should have the following columns:
- `username`
- `password`
- `expected_status` (success/failure)
