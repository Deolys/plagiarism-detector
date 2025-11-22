from pydantic import BaseModel, Field

class CodeCheckRequest(BaseModel):
    code: str = Field(..., description="Python code to check for plagiarism")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
            }
        }
