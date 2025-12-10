## AI Agent Interface Details for Selenium Pytest Automation

### 1. URL
- **Interface URL:** https://ai-agent.example.com/

### 2. Authentication Requirements
- **Type:** OAuth2 (Bearer Token)
- **Header:** `Authorization: Bearer <token>`
- **How to Obtain Token:**
  - Use provided test account credentials (see below) to authenticate via the `/auth` endpoint or obtain from environment variable `AI_AGENT_TEST_TOKEN`.

### 3. Main Selectors for Input and Output
- **Input Selector:**
  - `input[name='query']` (Main text field for submitting queries)
  - `button[type='submit']` (Submit button)
- **Output Selector:**
  - `div.response` (Container for agent's response)
  - `span.escalation` (Escalation message, if present)
  - `span.invalid-input` (Invalid input message, if present)
  - `span.handoff` (Handoff notification, if present)

### 4. Selenium Setup Steps
- Install required packages:
  - `pip install selenium pytest python-dotenv`
- Download and configure the appropriate WebDriver (e.g., ChromeDriver or GeckoDriver).
- Set environment variables (see below).
- Ensure network access to the AI agent's URL.

### 5. Environment Variables
- `AI_AGENT_TEST_TOKEN` (Bearer token for authentication)
- `AI_AGENT_TEST_URL` (Override default URL if needed)
- `AI_AGENT_TEST_USER` (Test account username)
- `AI_AGENT_TEST_PASS` (Test account password)

### 6. Test Accounts
- **Username:** testuser
- **Password:** TestPass123!
- These credentials can be used to obtain an OAuth2 token for API or UI login.

### 7. Additional Notes
- For edge case testing, ensure the test account has permissions to trigger escalation, invalid input, and handoff scenarios.
- If running in CI, set all environment variables in the runner configuration.
- For stress testing, confirm rate limits and session timeouts with the backend team.

---
**Contact:** Reach out to DevOps for test token refresh or additional test accounts.
