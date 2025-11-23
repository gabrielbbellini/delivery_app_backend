from fastapi import APIRouter, HTTPException
from src.view.schemas.freight import FreightCalcRequest
from src.domain.usecases.freight import FreightUseCases

router = APIRouter(prefix="/freight")

@router.post("/calc")
async def calculate_freight(payload: FreightCalcRequest):
    freight_uc = FreightUseCases()
    try:
        return await freight_uc.calculate_quote(payload)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))