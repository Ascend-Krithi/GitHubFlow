import pytest
import requests

BASE_URL = "https://example.com/api"

@pytest.fixture
def auth_token():
    """
    Fixture to obtain authentication token for authorized requests.
    Replace with actual login endpoint and credentials as needed.
    """
    login_url = f"{BASE_URL}/login"
    payload = {"username": "testuser", "password": "password123"}
    response = requests.post(login_url, json=payload)
    assert response.status_code == 200
    return response.json()["token"]

@pytest.fixture
def headers(auth_token):
    """
    Fixture to provide headers with authentication token.
    """
    return {"Authorization": f"Bearer {auth_token}"}

def test_full_valid_print_request(headers):
    """
    Test submitting a valid print request with all required metadata and default settings.
    Expects successful print job and confirmation message.
    """
    url = f"{BASE_URL}/print"
    payload = {
        "document_name": "TestDocument.pdf",
        "metadata": {"author": "QA", "pages": 2},
        "settings": {
            "paper_size": "A4",
            "duplex": False,
            "sides": "single"
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp.get("status") == "success"
    assert json_resp.get("settings", {}).get("paper_size") == "A4"
    assert json_resp.get("settings", {}).get("sides") == "single"
    assert "confirmation" in json_resp

def test_capability_supported_duplex_print(headers):
    """
    Test submitting a print request with duplex printing enabled if supported by the printer.
    Expects successful double-sided print job if supported, or skips if not supported.
    """
    # First, check printer capabilities
    capabilities_url = f"{BASE_URL}/printer/capabilities"
    capabilities_resp = requests.get(capabilities_url, headers=headers)
    assert capabilities_resp.status_code == 200
    capabilities = capabilities_resp.json()
    if not capabilities.get("duplex_supported", False):
        pytest.skip("Duplex printing not supported by the printer.")

    url = f"{BASE_URL}/print"
    payload = {
        "document_name": "TestDocumentDuplex.pdf",
        "metadata": {"author": "QA", "pages": 4},
        "settings": {
            "paper_size": "A4",
            "duplex": True,
            "sides": "double"
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp.get("status") == "success"
    assert json_resp.get("settings", {}).get("duplex") is True
    assert json_resp.get("settings", {}).get("sides") == "double"
    assert "confirmation" in json_resp

def test_missing_document_name(headers):
    """
    Test submitting a print request without a document name.
    Expects 400 Bad Request and specific error message.
    """
    url = f"{BASE_URL}/print"
    payload = {
        # "document_name" intentionally omitted
        "metadata": {"author": "QA", "pages": 1},
        "settings": {
            "paper_size": "A4",
            "duplex": False,
            "sides": "single"
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 400
    json_resp = response.json()
    assert json_resp.get("error") == "Missing required field: document_name."

def test_unsupported_paper_size(headers):
    """
    Test submitting a print request with an unsupported paper size.
    Expects 400 Bad Request and specific error message.
    """
    url = f"{BASE_URL}/print"
    payload = {
        "document_name": "UnsupportedPaperSize.pdf",
        "metadata": {"author": "QA", "pages": 2},
        "settings": {
            "paper_size": "A3",  # Unsupported
            "duplex": False,
            "sides": "single"
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 400
    json_resp = response.json()
    assert json_resp.get("error") == "Unsupported paper size selected. Please choose from: A4, Letter."

def test_user_not_authenticated():
    """
    Test submitting a print request without authentication.
    Expects 401 Unauthorized and specific error message.
    """
    url = f"{BASE_URL}/print"
    payload = {
        "document_name": "NoAuth.pdf",
        "metadata": {"author": "QA", "pages": 1},
        "settings": {
            "paper_size": "A4",
            "duplex": False,
            "sides": "single"
        }
    }
    # No headers provided, simulating unauthenticated user
    response = requests.post(url, json=payload)
    assert response.status_code == 401
    json_resp = response.json()
    assert json_resp.get("error") == "Authentication required. Please log in."
