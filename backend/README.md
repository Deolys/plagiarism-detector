# Plagiarism Detector API

AI-powered plagiarism detection system using 5 specialized agents built with FastAPI, LangChain, and OpenAI.

## Architecture

### 5 Specialized AI Agents

1. **Agent 1: Code Splitter** - Splits code into logical blocks (functions/classes)
2. **Agent 2: Git Searcher** - Searches for similar code on GitHub
3. **Agent 3: Similarity Finder** - Compares code blocks with found matches using LLM
4. **Agent 4: Plagiarism Judge** - (Coming soon) Provides final plagiarism verdict
5. **Agent 5: Report Builder** - (Coming soon) Generates detailed JSON report

## Setup

### Prerequisites

- Python 3.9+
- OpenAI API Key
- GitHub Token

### Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env`:
```
OPENAI_API_KEY=your_openai_key
GITHUB_TOKEN=your_github_token
GITHUB_API_URL=https://api.github.com
LOG_LEVEL=INFO
```

## Running the Server

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /api/v1/health
```

### Check Code for Plagiarism (JSON)
```
POST /api/v1/check
Content-Type: application/json

{
  "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
}
```

**Response:**
```json
{
  "success": true,
  "comparisons": [
    {
      "block_name": "fibonacci",
      "similarity_percent": 85,
      "source_repo": "github.com/user/repo",
      "source_url": "https://github.com/user/repo/blob/main/file.py",
      "reason": "Very similar implementation"
    }
  ]
}
```

### Check Code for Plagiarism (File Upload)
```
POST /api/v1/upload
Content-Type: multipart/form-data

file: <your_python_file.py>
```

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@example_code.py"
```

**Using Python:**
```python
import requests

with open('example_code.py', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/v1/upload', files=files)
    print(response.json())
```

**Or use the test script:**
```bash
python test_upload_endpoint.py example_code.py
```

**Response:** Same format as `/api/v1/check`

## Project Structure

```
app/
├── core/              # Configuration and exceptions
├── api/
│   └── v1/           # API v1 endpoints
├── agents/           # AI agents
│   ├── base/         # Base agent class
│   └── specialized/  # Specialized agents (1-5)
├── services/         # LLM, GitHub, code parsing services
├── schemas/          # Pydantic models
├── storage/          # In-memory storage
└── utils/            # Logging utilities
```

## Technologies

- **FastAPI** - Web framework
- **LangChain** - LLM interaction
- **LangGraph** - Agentic workflow orchestration
- **OpenAI** - Language model (gpt-3.5-turbo)
- **PyGithub** - GitHub API client
- **Pydantic** - Data validation

## Agent Pipeline (LangGraph)

The system uses LangGraph to orchestrate the three agents in a linear workflow:

```
START -> Code Splitter -> Git Searcher -> Similarity Finder -> END
         (Agent 1)         (Agent 2)         (Agent 3)
```

Each agent:
- Extends `BaseAgent` and `langchain_core.Runnable`
- Implements `invoke()` and `ainvoke()` methods
- Processes state through the graph
- Returns updated state with results

## Current Implementation Status

### ✅ Implemented
- Agent 1: Code Splitter (AST-based, LangGraph Runnable)
- Agent 2: Git Searcher (GitHub API, LangGraph Runnable)
- Agent 3: Similarity Finder (LLM-based comparison, LangGraph Runnable)
- LangGraph state machine orchestrator
- API endpoint `/api/v1/check`
- Health check endpoint

### ⏳ Upcoming
- Agent 4: Plagiarism Judge
- Agent 5: Report Builder
- Enhanced error handling and retry logic
- Result caching with Supabase
