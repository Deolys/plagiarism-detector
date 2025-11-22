from typing import Any, Dict, List
from langchain_core.runnables import Runnable
from app.agents.base.base_agent import BaseAgent
from app.services.github_service import github_service

class GitSearcherAgent(BaseAgent, Runnable):
    def __init__(self):
        super().__init__("GitSearcher")

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            blocks = input_data.get("blocks", [])
            self.log_info(f"Starting GitHub search for {len(blocks)} blocks...")

            search_results = []

            for block in blocks:
                code_lines = block["code"].split("\n")[:4]
                search_query = " ".join(code_lines).strip()[:200]

                if not search_query:
                    search_results.append({
                        "block_name": block["name"],
                        "block_type": block["type"],
                        "found_matches": []
                    })
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
