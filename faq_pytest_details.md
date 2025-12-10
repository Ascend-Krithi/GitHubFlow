Chat API Endpoint and Authentication:
- Endpoint: [PROVIDE_ENDPOINT_URL_HERE]
- Authentication: Typically via Bearer token in the Authorization header. Example:
  Authorization: Bearer <YOUR_API_TOKEN>
- The user is anonymous, so no user-specific credentials are required.

Knowledge Base Connection:
- Confirmed: The AI agent is connected to the FAQ knowledge base. This ensures responses to FAQ queries are grounded in the latest approved content and not generated from unsupported sources.

Expected Structure of Business Hours Response:
- Accuracy: Must match the official business hours as documented in the FAQ knowledge base.
- Conciseness: Directly answers the question without unnecessary elaboration.
- Politeness: Includes a courteous greeting or closing (e.g., "Thank you for your question!").
- Structure: Clearly formatted, e.g.:
  "Our business hours are Monday to Friday, 9:00 AM – 6:00 PM (America/New_York)."
- Timezone: Must include the IANA timezone format (e.g., America/New_York) or UTC offset (e.g., UTC-5).
- No Hallucinations: No extra, fabricated, or speculative information beyond the official FAQ content.

Measuring Response Latency in pytest:
- Use Python's time module to record the time before and after the API request.
- Example:
  import time
  start = time.time()
  response = requests.post(...)
  latency = time.time() - start
- Assert that latency <= 2.0 seconds.

Sample pytest Assertion:
assert latency <= 2.0, f"Response latency exceeded: {latency} seconds"

Summary: 
- Use the provided endpoint and authentication.
- Validate that the response is accurate, concise, polite, structured, and includes the timezone in the correct format.
- Measure and assert response latency is ≤ 2 seconds.
- Ensure no hallucinated or extraneous information is present in the response.
