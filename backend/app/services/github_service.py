from typing import List, Dict, Any
import re
from github import Github
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class GitHubService:
    def __init__(self):
        self.github = Github(settings.GITHUB_TOKEN)

    def _validate_query(self, query: str) -> str:
        """Validate and clean GitHub search query."""
        cleaned = re.sub(r'[^\w\s\-_.]', ' ', query)
        
        cleaned = ' '.join(cleaned.split())
        
        if len(cleaned.strip()) < 3:
            return ""
            
        return cleaned.strip()

    def search_code(self, query: str, language: str = "python", per_page: int = 3) -> List[Dict[str, Any]]:
        try:
            clean_query = self._validate_query(query)
            
            if not clean_query:
                logger.warning(f"Invalid or empty search query: '{query}'")
                return []
            
            search_query = f'{clean_query} language:{language}'
            logger.debug(f"GitHub search query: {search_query}")
            
            results = self.github.search_code(search_query, order="desc")

            matches = []
            for i, result in enumerate(results):
                if i >= per_page:
                    break

                matches.append({
                    "repo": result.repository.full_name,
                    "url": result.html_url,
                    "path": result.path,
                    "snippet": result.decoded_content[:500] if hasattr(result, 'decoded_content') else ""
                })

            return matches
        except Exception as e:
            logger.error(f"GitHub search error: {e}")
            return []

github_service = GitHubService()
