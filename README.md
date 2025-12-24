# Automation Test Scripts

This repository contains automated test scripts for the Print API.

## Structure
- IntegrationTests/: Contains integration test scripts for the Print API.
- test_doc.pdf: Sample document used for print job submission tests.
- print_api_test.log: Log file generated during test execution.

## How to Run
1. Ensure Python 3.x and pytest are installed.
2. Place a valid PDF file as 'test_doc.pdf' in the repo root.
3. Run tests with `pytest IntegrationTests/test_print_api.py`.