from fastapi import FastAPI
from db import creat_all_tables
from .routers import customers, invoices, trasactions

app = FastAPI(lifespan=creat_all_tables)
app.include_router(customers.router)
app.include_router(invoices.router)
app.include_router(trasactions.router)
