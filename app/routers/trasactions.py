from models import Transaction
from fastapi import APIRouter

router = APIRouter()

@router.post("/trasactions", tags=["Trasactions"])
async def create_trasactions(create_trasactions: Transaction):

    return create_trasactions
