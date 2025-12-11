# test_print_api.py
import pytest
import requests
import logging
from datetime import datetime

# Logging setup
logging.basicConfig(filename='test_print_api.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def log_test_case(name, input_params, expected, actual, result):
    logging.info(f"TEST CASE: {name}")
    logging.info(f"Input Parameters: {input_params}")
    logging.info(f"Expected Result: {expected}")
    logging.info(f"Actual Result: {actual}")
    logging.info(f"Result: {result}")
    logging.info('-'*60)

# API endpoints (replace with actual values)
API_BASE = "https://api.example.com/print"
AUTH_URL = f"{API_BASE}/auth"
PRINTERS_URL = f"{API_BASE}/printers"
JOBS_URL = f"{API_BASE}/jobs"

USERNAME = "test_agent"
PASSWORD = "secure_password"

# --- Helper functions ---
def authenticate(username, password):
    try:
        r = requests.post(AUTH_URL, json={"username": username, "password": password})
        r.raise_for_status()
        return r.json()["token"]
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        return None

def get_printer(token):
    try:
        r = requests.get(PRINTERS_URL, headers={"Authorization": f"Bearer {token}"})
        r.raise_for_status()
        printers = r.json().get("printers", [])
        assert printers, "No printers found"
        return printers[0]["id"]
    except Exception as e:
        logging.error(f"Get printer failed: {e}")
        return None

def get_capabilities(token, printer_id):
    try:
        r = requests.get(f"{PRINTERS_URL}/{printer_id}/capabilities", headers={"Authorization": f"Bearer {token}"})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logging.error(f"Get capabilities failed: {e}")
        return {}

def submit_print(token, printer_id, document, metadata, settings):
    headers = {"Authorization": f"Bearer {token}"}
    files = {"document": (document["filename"], document["content"], document["mimetype"])}
    data = {"metadata": str(metadata), "settings": str(settings)}
    try:
        r = requests.post(f"{JOBS_URL}/{printer_id}", headers=headers, files=files, data=data)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logging.error(f"Print job failed: {e}")
        return None

def example_document():
    return {"filename": "testdoc.txt", "content": b"Test print document.", "mimetype": "text/plain"}

def example_metadata():
    return {"title": "Test Print", "author": "Automation", "submitted_at": datetime.utcnow().isoformat()}

# --- Pytest fixtures ---
@pytest.fixture(scope="module")
def auth_token():
    token = authenticate(USERNAME, PASSWORD)
    assert token, "Authentication failed"
    return token

@pytest.fixture(scope="module")
def printer_id(auth_token):
    pid = get_printer(auth_token)
    assert pid, "No printer available"
    return pid

@pytest.fixture(scope="module")
def duplex_supported(auth_token, printer_id):
    caps = get_capabilities(auth_token, printer_id)
    return caps.get("duplex", False)

# --- Test cases ---
def test_full_valid_print_request(auth_token, printer_id):
    name = "Full Valid Print Request"
    doc = example_document()
    meta = example_metadata()
    settings = {"paper_size": "A4", "color": True, "duplex": False, "copies": 1}
    expected = "Print job submitted and confirmed."
    resp = submit_print(auth_token, printer_id, doc, meta, settings)
    actual = resp.get("status") if resp else None
    result = "Pass" if resp and actual == "confirmed" else "Fail"
    log_test_case(name, {"settings": settings}, expected, actual, result)
    assert result == "Pass"

def test_default_print_settings(auth_token, printer_id):
    name = "Default Print Settings"
    doc = example_document()
    meta = example_metadata()
    settings = {"paper_size": "Letter", "color": False, "duplex": False, "copies": 1}
    expected = "Print job submitted and confirmed."
    resp = submit_print(auth_token, printer_id, doc, meta, settings)
    actual = resp.get("status") if resp else None
    result = "Pass" if resp and actual == "confirmed" else "Fail"
    log_test_case(name, {"settings": settings}, expected, actual, result)
    assert result == "Pass"

def test_duplex_print_if_supported(auth_token, printer_id, duplex_supported):
    name = "Duplex Print If Supported"
    if not duplex_supported:
        pytest.skip("Duplex not supported")
    doc = example_document()
    meta = example_metadata()
    settings = {"paper_size": "A4", "color": False, "duplex": True, "copies": 1}
    expected = "Print job submitted and confirmed."
    resp = submit_print(auth_token, printer_id, doc, meta, settings)
    actual = resp.get("status") if resp else None
    result = "Pass" if resp and actual == "confirmed" else "Fail"
    log_test_case(name, {"settings": settings}, expected, actual, result)
    assert result == "Pass"
