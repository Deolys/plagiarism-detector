from fastapi import APIRouter, HTTPException, UploadFile, File
from app.schemas.report import CheckResponse, MatchInfo
from app.agents.orchestrator import Orchestrator
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()
orchestrator = Orchestrator()

@router.post("/upload", response_model=CheckResponse)
async def check_code_from_file(file: UploadFile = File(...)):
    """
    Upload a file and check its code for plagiarism.
    
    Accepts text files (preferably Python .py files) and processes them
    using the same pipeline as the /check endpoint.
    """
    try:
        logger.info(f"Received file upload request: {file.filename}")
        
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read file content
        try:
            content = await file.read()
            code = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400, 
                detail="File must be a text file with UTF-8 encoding"
            )
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            raise HTTPException(
                status_code=400, 
                detail=f"Error reading file: {str(e)}"
            )
        
        # Validate code content
        if not code or not code.strip():
            raise HTTPException(status_code=400, detail="File is empty or contains no code")
        
        logger.info(f"Processing file {file.filename} with {len(code)} characters")
        
        # Execute the same pipeline as /check endpoint
        result = orchestrator.execute_pipeline(code)
        
        if not result["success"]:
            return CheckResponse(
                success=False,
                error=result.get("error", "Unknown error occurred")
            )
        
        # Process comparisons
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
        
        logger.info(f"Successfully processed file {file.filename} with {len(comparisons)} comparisons")
        
        return CheckResponse(
            success=True,
            comparisons=comparisons
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in check_code_from_file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

