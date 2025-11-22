from pydantic import BaseModel
from typing import List, Optional

class MatchInfo(BaseModel):
    block_name: str
    similarity_percent: int
    source_repo: Optional[str] = None
    source_url: Optional[str] = None
    reason: Optional[str] = None

class CheckResponse(BaseModel):
    success: bool
    comparisons: List[MatchInfo] = []
    error: Optional[str] = None
