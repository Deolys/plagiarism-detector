# Quick Start Guide

## Installation

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `.env` file with your API keys:

```
OPENAI_API_KEY=sk-your-openai-key
GITHUB_TOKEN=ghp_your-github-token
GITHUB_API_URL=https://api.github.com
LOG_LEVEL=INFO
```

**How to get API keys:**

- **OpenAI**: Visit https://platform.openai.com/account/api-keys
- **GitHub Token**: Visit https://github.com/settings/tokens and create Personal Access Token

## Running the Server

```bash
python3 -m uvicorn app.main:app --reload
```

Server will start at `http://localhost:8000`

## Testing the API

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/v1/check" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
  }'
```

### Using Python Requests

```python
import requests

url = "http://localhost:8000/api/v1/check"
payload = {
    "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    def add(self, a, b):
        return a + b
"""
}

response = requests.post(url, json=payload)
print(response.json())
```

### Response Example

```json
{
  "success": true,
  "comparisons": [
    {
      "block_name": "fibonacci",
      "similarity_percent": 85,
      "source_repo": "github.com/algorithms/python",
      "source_url": "https://github.com/algorithms/python/blob/main/fib.py",
      "reason": "Very similar recursive implementation"
    },
    {
      "block_name": "add",
      "similarity_percent": 0,
      "source_repo": null,
      "source_url": null,
      "reason": null
    }
  ]
}
```

## API Documentation

### Swagger UI
```
http://localhost:8000/docs
```

### ReDoc
```
http://localhost:8000/redoc
```

## Understanding the Pipeline

1. **Code Splitter (Agent 1)**
   - Parses Python code using AST
   - Extracts functions and classes
   - Result: List of code blocks

2. **Git Searcher (Agent 2)**
   - Searches GitHub for each code block
   - Uses GitHub Code Search API
   - Result: List of similar code repositories

3. **Similarity Finder (Agent 3)**
   - Compares blocks with found matches using LLM
   - Calculates similarity percentage (0-100)
   - Result: Detailed comparison report

## Troubleshooting

### "Invalid API Key" Error
- Check OPENAI_API_KEY in .env file
- Ensure key starts with `sk-`

### "GitHub Token Invalid" Error
- Check GITHUB_TOKEN in .env file
- Token should start with `ghp_`

### "No Matches Found" Response
- Code might be unique or very different from public repos
- Try with well-known algorithms (fibonacci, bubble sort, etc.)

### Slow Performance
- First request is slower (LLM model warmup)
- GitHub API has rate limits (60 requests/hour unauthenticated)

## Next Steps

- See `LANGGRAPH_INTEGRATION.md` for architecture details
- Implement Agent 4 (Plagiarism Judge) and Agent 5 (Report Builder)
- Add Supabase for result caching
- Deploy to production with proper error handling
