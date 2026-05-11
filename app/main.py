from fastapi import FastAPI
from db import creat_all_tables
from .routers import customers, invoices, trasactions, plans

app = FastAPI(lifespan=creat_all_tables)
app.include_router(customers.router)
app.include_router(invoices.router)
app.include_router(trasactions.router)
app.include_router(plans.router)
