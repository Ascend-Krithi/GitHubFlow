# Automation-Test-Scripts

This repository contains automated test scripts for login functionality using Selenium, Pytest, and Openpyxl.

## Files
- test_login_selenium_excel.py: Main test script for login automation.
- login_test_data.xlsx: Sample Excel file containing test data.

## Usage
1. Install dependencies:
   ```bash
   pip install selenium openpyxl pytest
   ```
2. Download and set up ChromeDriver.
3. Update LOGIN_URL and element locators in the script as per your application.
4. Place the Excel file in the same directory.
5. Run the script with:
   ```bash
   pytest test_login_selenium_excel.py
   ```

## Test Data Example
| username      | password | expected_status |
|-------------- |--------- |----------------|
| mknaidu_user  | naidu    | success        |
| invalid_user  | naidu    | failure        |
| mknaidu_user  | wrong    | failure        |
|               |          | failure        |
