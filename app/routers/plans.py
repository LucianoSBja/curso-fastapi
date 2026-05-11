from sqlmodel import select

from fastapi import APIRouter

from db import SessionDep
from models import Plan

router = APIRouter()


@router.post("/plans", tags=["Plans"])
async def create_plan(plan_data:Plan , session: SessionDep):
    plan_data = Plan.model_validate(plan_data.model_dump())
    session.add(plan_data)
    session.commit()
    session.refresh(plan_data)
    return {"detail": "ok"}

@router.get("/plans", tags=["Plans"])
async def list_plans(session: SessionDep):
    plans = session.exec(select(Plan)).all()
    return plans
