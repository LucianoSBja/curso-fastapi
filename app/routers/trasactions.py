from sqlmodel import select

from db import SessionDep
from models import Customer, Transaction, TransactionCreate
from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.post("/trasactions", status_code=status.HTTP_201_CREATED, tags=["Trasactions"])
async def create_trasactions(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dic = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dic["customer_id"])
    if not customer:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    Transaction_db = Transaction.model_validate(transaction_data_dic)
    session.add(Transaction_db)
    session.commit()
    session.refresh(Transaction_db)
    return Transaction_db

@router.get("/trasactions", response_model=list[Transaction], tags=["Trasactions"])
async def list_transaction(session: SessionDep):
    query = select(Transaction)
    transactions = session.exec(query).all()
    return transactions
