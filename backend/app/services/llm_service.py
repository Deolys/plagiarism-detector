import json
from typing import Any
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.utils.logger import get_logger
import httpx



proxies = {
    'https': settings.PROXY
}

logger = get_logger(__name__)

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            http_client=httpx.Client(proxy=proxies.get('https')),
            # base_url=settings.OPENAI_API_BASE_URL,
            model="gpt-5-nano",
            temperature=0.3
        )

    def invoke(self, prompt: str) -> str:
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"LLM invocation error: {e}")
            raise

    def invoke_json(self, prompt: str) -> dict:
        response = self.invoke(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {response}")
            return {}

llm_service = LLMService()
