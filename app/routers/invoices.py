from fastapi import APIRouter
from models import Invoice

router = APIRouter()

@router.post("/invoices", tags=["Invoices"])
async def create_invoices(create_invoices: Invoice):

    return create_invoices
