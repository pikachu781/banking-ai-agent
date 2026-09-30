from fastapi import APIRouter
from pydantic import BaseModel

from app.services.emi_calculator import calculate_emi


router = APIRouter()


class EMIRequest(BaseModel):
    principal: float
    annual_rate: float
    years: float


@router.post("/calculate")
def calculate_emi_api(request: EMIRequest):

    result = calculate_emi(
        principal=request.principal,
        annual_rate=request.annual_rate,
        years=request.years
    )

    return result