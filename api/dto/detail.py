from pydantic import BaseModel


class DetailResponse(BaseModel):
    """
    DetailResponse represents response with detailed message
    """

    message: str
