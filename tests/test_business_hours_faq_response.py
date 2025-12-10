import pytest
import requests
import time
import re

# Test Case ID
TEST_CASE_ID = "TC-01"

# Chat API endpoint and authentication (replace with actual values)
API_ENDPOINT = "https://your-ai-agent-endpoint.com/chat"
API_TOKEN = "YOUR_API_TOKEN"

# Test data
QUERY_SENT = "What are your business hours?"

# Expected business hours (replace with actual FAQ values if different)
EXPECTED_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
EXPECTED_HOURS = "9:00 AM – 6:00 PM"
EXPECTED_TIMEZONE_PATTERN = r"\b(?:America\/[A-Za-z_]+|UTC[+-]?\d{0,2})\b"

def is_polite(response):
    polite_phrases = ["Thank you", "please", "You're welcome", "Let us know if you have any other questions"]
    return any(phrase in response for phrase in polite_phrases) or response.strip().endswith(".")

def is_concise(response):
    return len(response.split('.')) <= 2 and len(response) <= 200

def has_structured_content(response):
    days_present = any(day in response for day in EXPECTED_DAYS)
    hours_present = EXPECTED_HOURS.split("–")[0] in response and EXPECTED_HOURS.split("–")[1] in response
    timezone_present = re.search(EXPECTED_TIMEZONE_PATTERN, response) is not None
    return days_present and hours_present and timezone_present

def contains_hallucinated_info(response):
    # For this test, we assume any info outside expected days/hours/timezone is hallucinated
    # This can be improved with more FAQ context
    allowed_phrases = ["business hours", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "9:00 AM", "6:00 PM", "America/New_York", "UTC"]
    return not all(phrase in response or phrase.lower() in response.lower() for phrase in allowed_phrases)

@pytest.mark.timeout(3)
def test_business_hours_faq_response():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": QUERY_SENT,
        "user": "anonymous"
    }

    start_time = time.time()
    resp = requests.post(API_ENDPOINT, json=payload, headers=headers)
    latency = time.time() - start_time

    assert resp.status_code == 200, f"API returned status code {resp.status_code}"
    agent_response = resp.json().get("response", "").strip()

    # Validation Results
    accuracy = has_structured_content(agent_response)
    conciseness = is_concise(agent_response)
    politeness = is_polite(agent_response)
    structured_content = has_structured_content(agent_response)
    timezone_included = re.search(EXPECTED_TIMEZONE_PATTERN, agent_response) is not None
    response_latency = latency
    hallucinated_information = not contains_hallucinated_info(agent_response)

    print(f"Test Case ID: {TEST_CASE_ID}")
    print(f"Query Sent: '{QUERY_SENT}'")
    print(f"Agent Response: '{agent_response}'")
    print("Validation Results:")
    print(f"- Accuracy: {'Pass' if accuracy else 'Fail'}")
    print(f"- Conciseness: {'Pass' if conciseness else 'Fail'}")
    print(f"- Politeness: {'Pass' if politeness else 'Fail'}")
    print(f"- Structured Content: {'Pass' if structured_content else 'Fail'}")
    print(f"- Timezone Included: {'Pass' if timezone_included else 'Fail'}")
    print(f"- Response Latency: {response_latency:.2f} seconds")
    print(f"- Hallucinated Information: {'Pass' if hallucinated_information else 'Fail'}")

    assert accuracy, "Response does not accurately reflect business hours."
    assert conciseness, "Response is not concise."
    assert politeness, "Response is not polite."
    assert structured_content, "Response does not include structured content."
    assert timezone_included, "Timezone is not included in the response."
    assert response_latency <= 2.0, f"Response latency exceeded: {response_latency:.2f} seconds"
    assert hallucinated_information, "Response contains hallucinated information."

# To run the test, use: pytest -s <script_name.py>