from datetime import datetime
import zoneinfo

from fastapi import FastAPI, HTTPException, status
from models import Customer, CustomerCreate, Transaction, Invoice, CustomerUpdate
from db import SessionDep, creat_all_tables
from sqlmodel import select

app = FastAPI(lifespan=creat_all_tables)


@app.get("/")
async def root():
    return {"message": "Hola, Mundo!"}


country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    if not timezone_str:
        raise HTTPException(status_code=400, detail="Invalid country code")
    tz = zoneinfo.ZoneInfo(timezone_str)
    current_time = datetime.now(tz)
    formatted_time = current_time.strftime("%H:%M:%S")
    return {"country": iso, "time": formatted_time}

db_customers: list[Customer]=[]

@app.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CustomerCreate, session:SessionDep):
    customer= Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers", response_model=list[Customer])
async def list_customer(session:SessionDep):
    return session.exec(select(Customer)).all()

@app.get("/customers/{customer_id}")
async def customer_by_id(customer_id:int ,session:SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id:int ,session:SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
            )
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}

@app.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.sqlmodel_update(customer_data.model_dump(exclude_unset=True))
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.post("/trasactions")
async def create_trasactions(create_trasactions: Transaction):

    return create_trasactions


@app.post("/invoices")
async def create_invoices(create_invoices: Invoice):

    return create_invoices
