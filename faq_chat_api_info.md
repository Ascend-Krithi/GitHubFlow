API Endpoint:
POST /api/v1/chat/query

Expected Response Format:
{
  "response": "<string>",
  "source": "<string>",
  "latency_ms": <int>,
  "metadata": {
    "politeness": <bool>,
    "conciseness": <bool>,
    "structured": <bool>,
    "timezone_included": <bool>,
    "hallucination": <bool>
  }
}

FAQ Knowledge Base Connection:
The AI agent is confirmed to be connected to the FAQ knowledge base. All FAQ queries are answered using up-to-date information from this source.

Business Hours (as stored in the FAQ knowledge base):
Monday to Friday: 9:00 AM – 6:00 PM (Eastern Time)
Saturday & Sunday: Closed
