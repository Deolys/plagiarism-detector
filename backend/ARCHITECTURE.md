# System Architecture

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                     FASTAPI APPLICATION                    │
│                                                             │
│  POST /api/v1/check                                        │
│  ├─ Validate input code                                    │
│  ├─ Call orchestrator.execute_pipeline()                   │
│  └─ Return JSON response                                   │
│                                                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                 ORCHESTRATOR (LangGraph)                   │
│                                                             │
│          ┌─────────────────────────────────────┐           │
│          │     StateGraph(dict)                │           │
│          │                                     │           │
│          │  Nodes:                             │           │
│          │  1. code_splitter → _run_agent_1   │           │
│          │  2. git_searcher → _run_agent_2    │           │
│          │  3. similarity_finder → _run_agent_3│          │
│          │                                     │           │
│          │  Edges:                             │           │
│          │  START → code_splitter              │           │
│          │  → git_searcher → similarity_finder │           │
│          │  → END                              │           │
│          │                                     │           │
│          └─────────────────────────────────────┘           │
│                                                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────────┐
          │   Initial State (dict)   │
          │                          │
          │  {                       │
          │   "code": input_code,    │
          │   "blocks": [],          │
          │   "search_results": [],  │
          │   "comparisons": [],     │
          │   "success": True        │
          │  }                       │
          └──────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌────────┐   ┌────────┐   ┌────────┐
   │AGENT 1 │   │AGENT 2 │   │AGENT 3 │
   └────────┘   └────────┘   └────────┘
        │            │            │
        ▼            ▼            ▼
   ┌────────────────────────────────────┐
   │   Intermediate State Updates        │
   │                                    │
   │  After Agent 1:                    │
   │  ├─ blocks: list of code blocks    │
   │  └─ total_blocks: 2                │
   │                                    │
   │  After Agent 2:                    │
   │  ├─ search_results: matches list   │
   │  └─ (from GitHub API)              │
   │                                    │
   │  After Agent 3:                    │
   │  ├─ comparisons: similarity data   │
   │  ├─ is_suspicious: boolean flags   │
   │  └─ final success: true/false      │
   │                                    │
   └────────────────────────────────────┘
                     │
                     ▼
         ┌──────────────────────────┐
         │   Final State (dict)     │
         │                          │
         │  {                       │
         │   "success": true,       │
         │   "comparisons": [...],  │
         │   "total_blocks": 2,     │
         │   "stage_1_result": {...}│
         │   "stage_2_result": {...}│
         │   "stage_3_result": {...}│
         │  }                       │
         └──────────────────────────┘
                     │
                     ▼
         ┌──────────────────────────┐
         │   JSON API Response      │
         │                          │
         │  {                       │
         │   "success": true,       │
         │   "comparisons": [       │
         │     {                    │
         │      "block_name": "...",│
         │      "similarity": 85,   │
         │      "source_repo": "...",
         │      "source_url": "..."│
         │     }                    │
         │   ]                      │
         │  }                       │
         └──────────────────────────┘
```

## Agent Details

### Agent 1: Code Splitter

```python
┌──────────────────────────────────────────────┐
│        CodeSplitterAgent (Runnable)          │
└──────────────────────────────────────────────┘
          │
          ├─ Input: {"code": str}
          │
          ├─ Process:
          │   ├─ Parse code using AST
          │   ├─ Extract functions
          │   ├─ Extract classes
          │   └─ Create blocks list
          │
          └─ Output: {
               "blocks": [
                 {
                   "type": "function",
                   "name": "foo",
                   "code": "def foo(): ...",
                   "lines": (1, 5)
                 },
                 ...
               ],
               "total_blocks": 2
             }
```

### Agent 2: Git Searcher

```python
┌──────────────────────────────────────────────┐
│        GitSearcherAgent (Runnable)           │
└──────────────────────────────────────────────┘
          │
          ├─ Input: {"blocks": list}
          │
          ├─ Process (for each block):
          │   ├─ Extract first 4 lines as query
          │   ├─ Call GitHub Code Search API
          │   ├─ Fetch top 3 matches
          │   └─ Store matches with metadata
          │
          └─ Output: {
               "search_results": [
                 {
                   "block_name": "foo",
                   "found_matches": [
                     {
                       "repo": "user/repo",
                       "url": "github.com/...",
                       "path": "file.py",
                       "snippet": "def foo(): ..."
                     }
                   ]
                 }
               ]
             }
```

### Agent 3: Similarity Finder

```python
┌──────────────────────────────────────────────┐
│      SimilarityFinderAgent (Runnable)        │
└──────────────────────────────────────────────┘
          │
          ├─ Input: {
          │   "blocks": list,
          │   "search_results": list
          │ }
          │
          ├─ Process (for each block):
          │   ├─ Get found matches from search_results
          │   ├─ Compare with first match using LLM
          │   │  └─ Prompt GPT-3.5: "Compare similarity"
          │   ├─ Get similarity percentage (0-100)
          │   └─ Flag as suspicious if > 70%
          │
          └─ Output: {
               "comparisons": [
                 {
                   "block_name": "foo",
                   "block_type": "function",
                   "similarity_percent": 85,
                   "is_suspicious": true,
                   "source_repo": "user/repo",
                   "source_url": "github.com/...",
                   "reason": "Very similar recursive implementation"
                 }
               ]
             }
```

## Service Layer

```
┌─────────────────────────────────────────────────┐
│              SERVICE LAYER                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  LLMService                                     │
│  ├─ OpenAI Client (gpt-3.5-turbo)              │
│  ├─ invoke(prompt) → str                       │
│  └─ invoke_json(prompt) → dict                 │
│                                                 │
│  GitHubService                                  │
│  ├─ GitHub Client (PyGithub)                   │
│  └─ search_code(query, language) → list        │
│                                                 │
│  CodeParser                                     │
│  ├─ AST Parser                                 │
│  └─ parse_code(code) → list[blocks]            │
│                                                 │
└─────────────────────────────────────────────────┘
```

## State Management Pattern

```
State Dictionary Flow:

Step 1 - Initial State:
{
  "code": "def foo(): pass",
  "blocks": [],
  "search_results": [],
  "comparisons": [],
  "success": True
}
         │
         ▼ Agent 1 Processes
{
  "code": "def foo(): pass",
  "blocks": [{"name": "foo", "code": "...", ...}],
  "search_results": [],
  "comparisons": [],
  "success": True,
  "total_blocks": 1,
  "stage_1_result": {...}  ← Agent 1 result stored
}
         │
         ▼ Agent 2 Processes
{
  "code": "...",
  "blocks": [...],
  "search_results": [{"block_name": "foo", "found_matches": [...]}],
  "comparisons": [],
  "success": True,
  "total_blocks": 1,
  "stage_1_result": {...},
  "stage_2_result": {...}  ← Agent 2 result stored
}
         │
         ▼ Agent 3 Processes
{
  "code": "...",
  "blocks": [...],
  "search_results": [...],
  "comparisons": [{"block_name": "foo", "similarity_percent": 85, ...}],
  "success": True,
  "total_blocks": 1,
  "stage_1_result": {...},
  "stage_2_result": {...},
  "stage_3_result": {...}  ← Agent 3 result stored
}
```

## Error Handling Flow

```
Input Validation
    │
    ├─ Empty code? → 400 Bad Request
    │
    ▼
Agent 1: Code Splitter
    │
    ├─ Syntax Error? → Return error state
    │
    ▼
Agent 2: GitHub Search
    │
    ├─ API Error? → Return empty results
    │
    ▼
Agent 3: Similarity Finder
    │
    ├─ LLM Error? → Return default similarity
    │
    ▼
Return Final State → JSON Response
```

## Future Architecture (With Agents 4 & 5)

```
START → Agent 1 → Agent 2 → Agent 3 → Agent 4 → Agent 5 → END
        Splitter  Searcher  Finder     Judge    Reporter

Final State:
{
  "comparisons": [...],
  "plagiarism_verdict": {              ← Agent 4
    "is_plagiarism": true,
    "confidence": 92,
    "reasons": [...]
  },
  "report": {                          ← Agent 5
    "uniqueness_score": 35,
    "recommendation": "PLAGIARISM",
    "suspicious_fragments": [...]
  }
}
```

## Database Integration (Future)

```
FastAPI Endpoint
    │
    ├─ Check cache in Supabase
    │  (if code hash exists)
    │
    ├─ If miss: Execute pipeline
    │
    └─ Store results in Supabase
       {
         "code_hash": "...",
         "results": {...},
         "created_at": "...",
         "expires_at": "..."
       }
```
