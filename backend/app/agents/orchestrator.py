from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from app.agents.specialized.agent_1_code_splitter import CodeSplitterAgent
from app.agents.specialized.agent_2_git_searcher import GitSearcherAgent
from app.agents.specialized.agent_3_similarity_finder import SimilarityFinderAgent
from app.utils.logger import get_logger

logger = get_logger(__name__)

class Orchestrator:
    def __init__(self):
        self.agent_1 = CodeSplitterAgent()
        self.agent_2 = GitSearcherAgent()
        self.agent_3 = SimilarityFinderAgent()
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(dict)

        workflow.add_node("code_splitter", self._run_agent_1)
        workflow.add_node("git_searcher", self._run_agent_2)
        workflow.add_node("similarity_finder", self._run_agent_3)

        workflow.add_edge(START, "code_splitter")
        workflow.add_edge("code_splitter", "git_searcher")
        workflow.add_edge("git_searcher", "similarity_finder")
        workflow.add_edge("similarity_finder", END)

        return workflow.compile()

    def _run_agent_1(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Running Agent 1: Code Splitter")
        result = self.agent_1.invoke({"code": state.get("code", "")})

        if not result["success"]:
            logger.error(f"Agent 1 failed: {result.get('error')}")
            return {
                "success": False,
                "error": result.get("error"),
                "stage": "code_splitting"
            }

        logger.info(f"Agent 1 completed: {result['total_blocks']} blocks extracted")
        state.update({
            "blocks": result["blocks"],
            "total_blocks": result["total_blocks"],
            "stage_1_result": result
        })
        return state

    def _run_agent_2(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Running Agent 2: Git Searcher")
        result = self.agent_2.invoke({"blocks": state.get("blocks", [])})

        if not result["success"]:
            logger.error(f"Agent 2 failed: {result.get('error')}")
            return {
                "success": False,
                "error": result.get("error"),
                "stage": "git_search"
            }

        logger.info(f"Agent 2 completed: GitHub search finished")
        state.update({
            "search_results": result["search_results"],
            "stage_2_result": result
        })
        return state

    def _run_agent_3(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Running Agent 3: Similarity Finder")
        result = self.agent_3.invoke({
            "blocks": state.get("blocks", []),
            "search_results": state.get("search_results", [])
        })

        if not result["success"]:
            logger.error(f"Agent 3 failed: {result.get('error')}")
            return {
                "success": False,
                "error": result.get("error"),
                "stage": "similarity_analysis"
            }

        logger.info(f"Agent 3 completed: similarity analysis finished")
        state.update({
            "comparisons": result["comparisons"],
            "stage_3_result": result,
            "success": True
        })
        return state

    def execute_pipeline(self, code: str) -> Dict[str, Any]:
        logger.info("=== Starting Plagiarism Detection Pipeline ===")

        initial_state = {
            "code": code,
            "blocks": [],
            "search_results": [],
            "comparisons": [],
            "success": True
        }

        final_state = self.graph.invoke(initial_state)

        logger.info("=== Pipeline Completed ===")

        return {
            "success": final_state.get("success", False),
            "error": final_state.get("error"),
            "comparisons": final_state.get("comparisons", []),
            "total_blocks": final_state.get("total_blocks", 0),
            "stage_1_result": final_state.get("stage_1_result"),
            "stage_2_result": final_state.get("stage_2_result"),
            "stage_3_result": final_state.get("stage_3_result")
        }
