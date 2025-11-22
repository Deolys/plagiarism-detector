# LangGraph Integration Guide

## Overview

The plagiarism detector uses **LangGraph** for orchestrating the three AI agents in a state-based workflow. Each agent is implemented as a `langchain_core.Runnable`, allowing seamless integration with the LangGraph state machine.

## Agent Architecture

### Base Agent Class (`BaseAgent`)

All agents inherit from `BaseAgent` and `langchain_core.Runnable`:

```python
from langchain_core.runnables import Runnable

class CodeSplitterAgent(BaseAgent, Runnable):
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Process input and return state
        pass

    async def ainvoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Async version (returns sync result)
        pass

    @property
    def InputType(self):
        return Dict[str, Any]

    @property
    def OutputType(self):
        return Dict[str, Any]
```

## Graph Structure

### LangGraph State Machine

The orchestrator builds a linear workflow using `StateGraph`:

```python
from langgraph.graph import StateGraph, START, END

workflow = StateGraph(dict)

# Add nodes
workflow.add_node("code_splitter", self._run_agent_1)
workflow.add_node("git_searcher", self._run_agent_2)
workflow.add_node("similarity_finder", self._run_agent_3)

# Define edges
workflow.add_edge(START, "code_splitter")
workflow.add_edge("code_splitter", "git_searcher")
workflow.add_edge("git_searcher", "similarity_finder")
workflow.add_edge("similarity_finder", END)

# Compile
graph = workflow.compile()
```

### State Flow

```
Initial State (code)
        ↓
   [Agent 1: Code Splitter]
        → blocks
        ↓
   [Agent 2: Git Searcher]
        → search_results
        ↓
   [Agent 3: Similarity Finder]
        → comparisons
        ↓
   Final State (all results)
```

## Executing the Pipeline

```python
orchestrator = Orchestrator()

result = orchestrator.execute_pipeline(code_string)

print(result["comparisons"])  # List of similarity results
print(result["total_blocks"]) # Number of code blocks
```

## Agent Details

### Agent 1: Code Splitter
- **Input**: `{"code": str}`
- **Output**: `{"blocks": list, "total_blocks": int, ...}`
- **Function**: Parses Python code using AST and extracts functions/classes

### Agent 2: Git Searcher
- **Input**: `{"blocks": list}`
- **Output**: `{"search_results": list, ...}`
- **Function**: Searches GitHub for similar code snippets

### Agent 3: Similarity Finder
- **Input**: `{"blocks": list, "search_results": list}`
- **Output**: `{"comparisons": list, ...}`
- **Function**: Uses LLM to compare code similarity

## State Management

Each node in the graph receives and returns the full state dictionary:

```python
def _run_agent_1(self, state: Dict[str, Any]) -> Dict[str, Any]:
    # Extract from state
    code = state.get("code", "")

    # Process
    result = self.agent_1.invoke({"code": code})

    # Update state
    state.update({
        "blocks": result["blocks"],
        "total_blocks": result["total_blocks"]
    })

    return state
```

## Key Benefits of LangGraph

1. **State-Based Workflow**: Each agent operates on and modifies the shared state
2. **Linear Execution**: Clear sequence of agent operations
3. **Error Handling**: Can add conditional edges based on state
4. **Logging**: Built-in support for debugging and monitoring
5. **Extensibility**: Easy to add new agents or modify flow

## Future Enhancements

- Conditional edges based on code complexity
- Parallel processing of blocks
- Result caching at intermediate stages
- Retry logic with exponential backoff
