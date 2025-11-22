from fastapi import APIRouter, HTTPException
from app.schemas.code_check import CodeCheckRequest
from app.schemas.report import CheckResponse, MatchInfo
from app.agents.orchestrator import Orchestrator
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()
orchestrator = Orchestrator()

@router.post("/check", response_model=CheckResponse)
def check_code(request: CodeCheckRequest):
    try:
        logger.info("Received code check request")

        if not request.code or not request.code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")

        result = orchestrator.execute_pipeline(request.code)

        if not result["success"]:
            return CheckResponse(
                success=False,
                error=result.get("error", "Unknown error occurred")
            )

        comparisons_data = result.get("comparisons", [])
        comparisons = [
            MatchInfo(
                block_name=comp["block_name"],
                similarity_percent=comp.get("similarity_percent", 0),
                source_repo=comp.get("source_repo"),
                source_url=comp.get("source_url"),
                reason=comp.get("reason")
            )
            for comp in comparisons_data
        ]

        return CheckResponse(
            success=True,
            comparisons=comparisons
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in check_code: {e}")
        raise HTTPException(status_code=500, detail=str(e))
