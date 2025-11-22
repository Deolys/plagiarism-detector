from typing import Any, Dict, List
from langchain_core.runnables import Runnable
from app.agents.base.base_agent import BaseAgent
from app.services.code_parser import code_parser
from app.core.exceptions import CodeParseError

class CodeSplitterAgent(BaseAgent, Runnable):
    def __init__(self):
        super().__init__("CodeSplitter")

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            code = input_data.get("code", "")
            self.log_info("Starting code splitting...")

            blocks = code_parser.parse_code(code)

            self.log_info(f"Successfully split code into {len(blocks)} blocks")

            return {
                "success": True,
                "total_blocks": len(blocks),
                "blocks": blocks,
                "code": code
            }
        except CodeParseError as e:
            self.log_error(f"Code parsing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "total_blocks": 0,
                "blocks": [],
                "code": input_data.get("code", "")
            }
        except Exception as e:
            self.log_error(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": str(e),
                "total_blocks": 0,
                "blocks": [],
                "code": input_data.get("code", "")
            }

    async def ainvoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.invoke(input_data)

    @property
    def InputType(self):
        return Dict[str, Any]

    @property
    def OutputType(self):
        return Dict[str, Any]
