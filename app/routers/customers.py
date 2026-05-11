from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select

from models import Customer, CustomerCreate, CustomerUpdate, Plan, CustomerPlan, StatusEnum
from db import SessionDep

router = APIRouter()

@router.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["Customers"])
async def create_customer(customer_data: CustomerCreate, session:SessionDep):
    customer= Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers", response_model=list[Customer], tags=["Customers"])
async def list_customer(session:SessionDep):
    return session.exec(select(Customer)).all()

@router.get("/customers/{customer_id}", tags=["Customers"])
async def customer_by_id(customer_id:int ,session:SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

@router.delete("/customers/{customer_id}",tags=["Customers"])
async def delete_customer(customer_id:int ,session:SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
            )
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}

@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["Customers"])
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.sqlmodel_update(customer_data.model_dump(exclude_unset=True))
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.post("/customers/{customer_id}/subscribe/{plan_id}", response_model=Customer, tags=["Customers"])
async def subscribe_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep,  plan_status:StatusEnum = Query() ):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    plan = session.get(Plan, plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    customer_plan = CustomerPlan(
        customer_id=customer_id,
        plan_id=plan_id,
        status=plan_status
        )

    session.add(customer_plan)
    session.commit()
    session.refresh(customer_plan)
    return customer_plan


@router.get("/customers/{customer_id}/subscribe", response_model=Customer, tags=["Customers"])
async def subscribe_customer_plan(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)

    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.status == StatusEnum.ACTIVE)
        )

    customer_plans = session.exec(query).all()
    return customer_plans
