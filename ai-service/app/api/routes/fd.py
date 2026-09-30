from fastapi import APIRouter
from pydantic import BaseModel

from app.services.fd_calculator import calculate_fd


router = APIRouter()


class FDRequest(BaseModel):
    principal: float
    rate: float
    years: float


@router.post("/calculate")
def calculate_fd_api(request: FDRequest):

    result = calculate_fd(
        principal=request.principal,
        rate=request.rate,
        years=request.years
    )

    return result