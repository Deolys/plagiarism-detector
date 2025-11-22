from typing import Any, Dict
from langchain_core.runnables import RunnableConfig
from app.utils.logger import get_logger

logger = get_logger(__name__)

class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(self.name)

    def log_info(self, message: str):
        self.logger.info(f"[{self.name}] {message}")

    def log_error(self, message: str):
        self.logger.error(f"[{self.name}] {message}")
