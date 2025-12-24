import requests
import pytest
import logging
from datetime import datetime
import time

# =========================
# Configuration & Constants
# =========================

API_BASE_URL = "https://api.example.com/print"
AGENT_CREDENTIALS = {"username": "test_agent", "password": "secure_password"}
DOCUMENT_PATH = "test_doc.pdf"  # Path to a valid test document
LOG_FILE = "print_api_test.log"

# =========================
# Logging Setup
# =========================

logging.basicConfig(
    filename=LOG_FILE