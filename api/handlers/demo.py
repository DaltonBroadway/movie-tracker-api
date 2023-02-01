from fastapi import APIRouter

from api.dto.detail import DetailResponse

router = APIRouter(prefix="/api/v1/demo")


@router.get("/", response_model=DetailResponse)
def hello_world():
    """
    Hello World endpoint
    """
    return DetailResponse(message="Hello World")
