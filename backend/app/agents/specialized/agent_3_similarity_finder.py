import json
from typing import Any, Dict, List
from langchain_core.runnables import Runnable
from app.agents.base.base_agent import BaseAgent
from app.services.llm_service import llm_service

class SimilarityFinderAgent(BaseAgent, Runnable):
    def __init__(self):
        super().__init__("SimilarityFinder")

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            blocks = input_data.get("blocks", [])
            search_results = input_data.get("search_results", [])
            self.log_info(f"Starting similarity analysis for {len(blocks)} blocks...")

            comparisons = []

            for i, block in enumerate(blocks):
                if i >= len(search_results):
                    break

                matches = search_results[i].get("found_matches", [])

                if not matches:
                    self.log_info(f"Block '{block['name']}': no matches to compare")
                    comparisons.append({
                        "block_name": block["name"],
                        "block_type": block["type"],
                        "similarity_percent": 0,
                        "is_suspicious": False,
                        "source": None,
                        "source_repo": None,
                        "source_url": None
                    })
                    continue

                first_match = matches[0]
                block_code = block["code"][:500]
                match_snippet = first_match.get("snippet", "")[:500]

                prompt = f"""Compare these two code snippets and determine similarity percentage.

Student Code:
```python
{block_code}
```

Found Code on GitHub:
```python
{match_snippet}
```

Respond ONLY with valid JSON (no markdown, no extra text):
{{
    "similarity_percent": <0-100>,
    "is_suspicious": <true or false>,
    "reason": "<brief reason>"
}}"""

                response = llm_service.invoke_json(prompt)

                similarity = response.get("similarity_percent", 0)
                is_suspicious = response.get("is_suspicious", False)

                comparisons.append({
                    "block_name": block["name"],
                    "block_type": block["type"],
                    "similarity_percent": similarity,
                    "is_suspicious": is_suspicious or similarity > 70,
                    "source": first_match.get("repo", ""),
                    "source_repo": first_match.get("repo", ""),
                    "source_url": first_match.get("url", ""),
                    "reason": response.get("reason", "")
                })

                self.log_info(f"Block '{block['name']}': {similarity}% similarity with {first_match.get('repo', 'unknown')}")

            self.log_info(f"Similarity analysis completed")

            return {
                "success": True,
                "comparisons": comparisons,
                "blocks": blocks,
                "search_results": search_results
            }
        except Exception as e:
            self.log_error(f"Similarity analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "comparisons": [],
                "blocks": input_data.get("blocks", []),
                "search_results": input_data.get("search_results", [])
            }

    async def ainvoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.invoke(input_data)

    @property
    def InputType(self):
        return Dict[str, Any]

    @property
    def OutputType(self):
        return Dict[str, Any]
