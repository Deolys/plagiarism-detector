from typing import List, Dict, Any
from github import Github
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class GitHubService:
    def __init__(self):
        self.github = Github(settings.GITHUB_TOKEN)

    def search_code(self, query: str, language: str = "python", per_page: int = 3) -> List[Dict[str, Any]]:
        try:
            search_query = f'{query} language:{language}'
            results = self.github.search_code(search_query, sort="stars", order="desc")

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
