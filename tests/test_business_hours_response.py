import pytest
import requests
import time

# Test Case ID
TEST_CASE_ID = "TC-01"

# API endpoint for the AI agent
API_URL = "http://localhost:8000/api/v1/chat/query"  # Replace with actual endpoint if different

# Expected business hours from FAQ knowledge base
EXPECTED_BUSINESS_HOURS = {
    "days": "Monday to Friday",
    "hours": "9:00 AM – 6:00 PM",
    "timezone": "Eastern Time",
    "weekend": "Closed"
}

# User query
QUERY_SENT = "What are your business hours?"

def validate_structured_content(response_text):
    """Checks if the response contains days, hours, and timezone information."""
    return (
        EXPECTED_BUSINESS_HOURS["days"] in response_text and
        EXPECTED_BUSINESS_HOURS["hours"] in response_text and
        EXPECTED_BUSINESS_HOURS["timezone"] in response_text
    )

def validate_conciseness(response_text):
    """Checks if the response is concise (≤ 2 sentences)."""
    sentences = [s for s in response_text.split('.') if s.strip()]
    return len(sentences) <= 2

def validate_politeness(response_text):
    """Checks for polite phrasing."""
    return any(phrase in response_text.lower() for phrase in ["our business hours", "please", "thank you"])

def validate_timezone_included(response_text):
    """Checks if timezone is mentioned."""
    return EXPECTED_BUSINESS_HOURS["timezone"].lower() in response_text.lower()

def validate_accuracy(response_text):
    """Checks if the response matches the FAQ knowledge base."""
    return (
        EXPECTED_BUSINESS_HOURS["days"] in response_text and
        EXPECTED_BUSINESS_HOURS["hours"] in response_text and
        EXPECTED_BUSINESS_HOURS["timezone"] in response_text and
        EXPECTED_BUSINESS_HOURS["weekend"].lower() in response_text.lower()
    )

def validate_hallucination(metadata):
    """Checks if the agent claims hallucinated information."""
    return metadata.get("hallucination", False) is False

@pytest.mark.timeout(2)
def test_business_hours_response():
    # Start timer for latency measurement
    start_time = time.time()
    payload = {
        "query": QUERY_SENT,
        "user": "anonymous"
    }
    response = requests.post(API_URL, json=payload)
    latency = time.time() - start_time

    assert response.status_code == 200, "Agent API did not return 200 OK"
    data = response.json()

    agent_response = data.get("response", "")
    metadata = data.get("metadata", {})
    latency_ms = data.get("latency_ms", int(latency * 1000))

    # Validation checks
    accuracy = validate_accuracy(agent_response)
    conciseness = validate_conciseness(agent_response)
    politeness = validate_politeness(agent_response)
    structured_content = validate_structured_content(agent_response)
    timezone_included = validate_timezone_included(agent_response)
    hallucinated_info = validate_hallucination(metadata)
    response_latency = latency_ms / 1000.0

    # Print output in required format
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
    print(f"- Hallucinated Information: {'Pass' if hallucinated_info else 'Fail'}")

    # Pytest assertions
    assert accuracy, "Accuracy validation failed"
    assert conciseness, "Conciseness validation failed"
    assert politeness, "Politeness validation failed"
    assert structured_content, "Structured content validation failed"
    assert timezone_included, "Timezone inclusion validation failed"
    assert response_latency <= 2, "Response latency exceeded 2 seconds"
    assert hallucinated_info, "Hallucinated information detected"

if __name__ == "__main__":
    # For manual run outside pytest
    test_business_hours_response()