import requests
import time
import pytest
import logging

# --- Configuration ---
API_URL = "https://api.printingsystem.example.com/v1"
TOKEN = "your_token_here"  # Replace with a valid token
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
DOCUMENT_URL = "https://files.example.com/docs/test_doc.pdf"  # Replace with a valid document URL

# --- Logging Setup ---
logging.basicConfig(
    filename='print_test_log.txt',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def log_test_case(name, input_params, expected, actual, status):
    log_entry = (
        f"Test Case: {name}\n"
        f"Input Parameters: {input_params}\n"
        f"Expected Result: {expected}\n"
        f"Actual Result: {actual}\n"
        f"Status: {status}\n"
        f"{'-'*60}"
    )
    logging.info(log_entry)
    print(log_entry)

# --- Helper Functions ---
def get_online_printer(duplex_required=False):
    resp = requests.get(f"{API_URL}/printers", headers=HEADERS)
    resp.raise_for_status()
    printers = resp.json()
    for printer in printers:
        if printer['status'] == 'online':
            if duplex_required and printer['capabilities'].get('duplex'):
                return printer
            elif not duplex_required:
                return printer
    return None

def submit_print_job(printer_id, settings):
    payload = {
        "document_url": DOCUMENT_URL,
        "printer_id": printer_id,
        "settings": settings
    }
    resp = requests.post(f"{API_URL}/print/jobs", headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()['job_id']

def poll_job_status(job_id, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(f"{API_URL}/print/jobs/{job_id}", headers=HEADERS)
        resp.raise_for_status()
        job = resp.json()
        if job['status'] in ['completed', 'failed']:
            return job
        time.sleep(2)
    raise TimeoutError("Print job status polling timed out.")

# --- Pytest Test Cases ---
@pytest.mark.parametrize("test_case", [
    {
        "name": "Full Valid Print Request (Default Settings)",
        "settings": {"copies": 1, "color": "mono", "duplex": False, "paper_size": "A4"},
        "duplex_required": False,
        "expected_status": "completed"
    },
    {
        "name": "Default Print Settings (Single-sided, Standard Paper)",
        "settings": {"copies": 1, "color": "mono", "duplex": False, "paper_size": "A4"},
        "duplex_required": False,
        "expected_status": "completed"
    },
    {
        "name": "Duplex Print (If Supported)",
        "settings": {"copies": 1, "color": "mono", "duplex": True, "paper_size": "A4"},
        "duplex_required": True,
        "expected_status": "completed"
    }
])
def test_print_operations(test_case):
    input_params = {
        "document_url": DOCUMENT_URL,
        "settings": test_case["settings"]
    }
    expected = f"Document is printed successfully with settings: {test_case['settings']}"
    actual = ""
    status = "Fail"
    try:
        # Step 1: Get a suitable printer
        printer = get_online_printer(test_case["duplex_required"])
        assert printer is not None, "No suitable printer found"
        input_params["printer_id"] = printer["printer_id"]

        # Step 2: Submit print job
        job_id = submit_print_job(printer["printer_id"], test_case["settings"])
        assert job_id, "Failed to submit print job"

        # Step 3: Poll job status
        job_result = poll_job_status(job_id)
        actual_status = job_result['status']
        actual_settings = job_result['settings']

        # Step 4: Assertions and logging
        assert actual_status == test_case["expected_status"], f"Expected status '{test_case['expected_status']}', got '{actual_status}'"
        for key, value in test_case["settings"].items():
            assert actual_settings[key] == value, f"Expected setting '{key}': {value}, got {actual_settings[key]}"

        actual = f"Document printed successfully with settings: {actual_settings}"
        status = "Pass"
    except Exception as e:
        actual = f"Error: {str(e)}"
        status = "Fail"
    finally:
        log_test_case(test_case["name"], input_params, expected, actual, status)
        assert status == "Pass", actual

# --- Run tests directly (optional) ---
if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__]))