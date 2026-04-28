from datetime import datetime
import zoneinfo

from fastapi import FastAPI, HTTPException
from models import Customer, Transaction, Invoice
from db import creat_all_tables
from .routers import customers

app = FastAPI(lifespan=creat_all_tables)
app.include_router(customers.router)


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

@app.post("/trasactions")
async def create_trasactions(create_trasactions: Transaction):

    return create_trasactions


@app.post("/invoices")
async def create_invoices(create_invoices: Invoice):

    return create_invoices
