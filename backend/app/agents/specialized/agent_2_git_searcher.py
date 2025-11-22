from typing import Any, Dict, List
import re
from langchain_core.runnables import Runnable
from app.agents.base.base_agent import BaseAgent
from app.services.github_service import github_service

class GitSearcherAgent(BaseAgent, Runnable):
    def __init__(self):
        super().__init__("GitSearcher")

    def _clean_search_query(self, code: str) -> str:
        """Extract meaningful keywords from code for GitHub search."""
        lines = code.split("\n")[:4]
        text = " ".join(lines)
        
        stop_words = {'def', 'class', 'self', 'import', 'from', 'return', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'with', 'as'}
        
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]{2,}\b', text)
        
        keywords = [w for w in words if w not in stop_words and not w.startswith('_')]
        
        query = " ".join(keywords[:5])
        
        return query.strip()[:200] if query.strip() else ""

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            blocks = input_data.get("blocks", [])
            self.log_info(f"Starting GitHub search for {len(blocks)} blocks...")

            search_results = []

            for block in blocks:
                search_query = self._clean_search_query(block["code"])
                
                if not search_query and block.get("name"):
                    search_query = re.sub(r'[^a-zA-Z0-9_\s]', '', block["name"])

                if not search_query:
                    search_results.append({
                        "block_name": block["name"],
                        "block_type": block["type"],
                        "found_matches": []
                    })
                    self.log_info(f"Block '{block['name']}': skipped (no valid search terms)")
                    continue

                matches = github_service.search_code(search_query, language="python", per_page=3)

                search_results.append({
                    "block_name": block["name"],
                    "block_type": block["type"],
                    "search_query": search_query[:100],
                    "found_matches": matches
                })

                self.log_info(f"Block '{block['name']}': found {len(matches)} matches")

            self.log_info(f"GitHub search completed. Total matches found: {sum(len(r['found_matches']) for r in search_results)}")

            return {
                "success": True,
                "search_results": search_results,
                "blocks": blocks
            }
        except Exception as e:
            self.log_error(f"GitHub search failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "search_results": [],
                "blocks": input_data.get("blocks", [])
            }

    async def ainvoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.invoke(input_data)

    @property
    def InputType(self):
        return Dict[str, Any]

    @property
    def OutputType(self):
        return Dict[str, Any]
