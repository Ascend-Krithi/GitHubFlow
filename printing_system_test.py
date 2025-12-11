# printing_system_test.py

import requests
import pytest
import time
import logging

# --- CONFIGURATION ---

API_BASE_URL = "https://your-printing-system.example.com/api/v1"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"
PRINTER_ID = "printer-12345"
DOCUMENT_URL = "https://example.com/files/test_doc.pdf"
DEFAULT_PAPER_SIZE = "A4"
DEFAULT_COPIES = 1
DEFAULT_COLOR = False

# Logging setup
logging.basicConfig(
    filename="printing_system_test.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# --- UTILITY FUNCTIONS ---

def api_headers():
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

def log_test_case(name, input_params, expected, actual, status):
    log_entry = (
        f"\nTEST CASE: {name}\n"
        f"Input Parameters: {input_params}\n"
        f"Expected Result: {expected}\n"
        f"Actual Result: {actual}\n"
        f"Status: {status}\n"
        f"{'-'*60}\n"
    )
    logging.info(log_entry)
    print(log_entry)

def get_printer_capabilities(printer_id):
    url = f"{API_BASE_URL}/printers/{printer_id}/capabilities"
    resp = requests.get(url, headers=api_headers())
    resp.raise_for_status()
    return resp.json()

def submit_print_job(printer_id, document_url, copies, duplex, color, paper_size, job_name):
    url = f"{API_BASE_URL}/print-jobs"
    payload = {
        "printer_id": printer_id,
        "document_url": document_url,
        "copies": copies,
        "duplex": duplex,
        "color": color,
        "paper_size": paper_size,
        "job_name": job_name
    }
    resp = requests.post(url, headers=api_headers(), json=payload)
    return resp

def poll_print_job_status(job_id, timeout=60, poll_interval=3):
    url = f"{API_BASE_URL}/print-jobs/{job_id}"
    start_time = time.time()
    while time.time() - start_time < timeout:
        resp = requests.get(url, headers=api_headers())
        resp.raise_for_status()
        status = resp.json().get("status")
        if status in ("completed", "failed", "cancelled"):
            return resp.json()
        time.sleep(poll_interval)
    return {"status": "timeout"}

# --- TEST CASES ---

@pytest.fixture(scope="module")
def printer_capabilities():
    return get_printer_capabilities(PRINTER_ID)

def test_full_valid_print_request(printer_capabilities):
    """
    Test a full valid print request with all required metadata and default settings.
    """
    test_name = "Full Valid Print Request"
    input_params = {
        "printer_id": PRINTER_ID,
        "document_url": DOCUMENT_URL,
        "copies": DEFAULT_COPIES,
        "duplex": False,
        "color": DEFAULT_COLOR,
        "paper_size": DEFAULT_PAPER_SIZE,
        "job_name": "test_doc_full_valid"
    }
    expected = "Document is printed successfully with default settings."

    resp = submit_print_job(**input_params)
    if resp.status_code != 200:
        actual = f"Failed to submit print job: {resp.text}"
        log_test_case(test_name, input_params, expected, actual, "Fail")
        assert False, actual

    job_info = resp.json()
    job_id = job_info.get("job_id")
    status_info = poll_print_job_status(job_id)
    actual_status = status_info.get("status")

    actual = f"Document printed with status: {actual_status}"
    status = "Pass" if actual_status == "completed" else "Fail"
    log_test_case(test_name, input_params, expected, actual, status)
    assert actual_status == "completed", f"Print job failed or not completed: {status_info}"

def test_default_print_settings(printer_capabilities):
    """
    Test print with default settings (standard paper size, single-sided).
    """
    test_name = "Default Print Settings"
    input_params = {
        "printer_id": PRINTER_ID,
        "document_url": DOCUMENT_URL,
        "copies": DEFAULT_COPIES,
        "duplex": False,
        "color": DEFAULT_COLOR,
        "paper_size": DEFAULT_PAPER_SIZE,
        "job_name": "test_doc_default_settings"
    }
    expected = "Document is printed successfully with default settings."

    resp = submit_print_job(**input_params)
    if resp.status_code != 200:
        actual = f"Failed to submit print job: {resp.text}"
        log_test_case(test_name, input_params, expected, actual, "Fail")
        assert False, actual

    job_info = resp.json()
    job_id = job_info.get("job_id")
    status_info = poll_print_job_status(job_id)
    actual_status = status_info.get("status")

    actual = f"Document printed with status: {actual_status}"
    status = "Pass" if actual_status == "completed" else "Fail"
    log_test_case(test_name, input_params, expected, actual, status)
    assert actual_status == "completed", f"Print job failed or not completed: {status_info}"

def test_duplex_printing_if_supported(printer_capabilities):
    """
    Test duplex printing if the printer supports it.
    """
    test_name = "Duplex Printing (If Supported)"
    duplex_supported = printer_capabilities.get("duplex_supported", False)
    input_params = {
        "printer_id": PRINTER_ID,
        "document_url": DOCUMENT_URL,
        "copies": DEFAULT_COPIES