from typing import List
from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from routers import tender, bid 
from database import engine, SessionLocal, get_db
from models import Base
from crud import get_organizations,  get_employees
from schemas import EmployeeBase, OrganizationBase
from demo import create_initial_data



app = FastAPI()


app.include_router(tender.router)
app.include_router(bid.router)

@app.on_event("startup")
async def on_startup():

    Base.metadata.create_all(bind=engine)
    

    db = SessionLocal()
    try:
        create_initial_data(db)
    finally:
        db.close()

@app.get("/api/ping", response_model=str)
async def ping():
    return "ok"

@app.get("/employees", response_model=List[EmployeeBase])
async def list_employees(
    skip: int = Query(0, alias="page", ge=0), 
    limit: int = Query(10, le=100), 
    db: Session = Depends(get_db),
    ):
    employees = get_employees(db, skip=skip, limit=limit)
    return employees

@app.get("/organizations", response_model=List[OrganizationBase])
async def list_organizations(
    skip: int = Query(0, alias="page", ge=0),
      limit: int = Query(10, le=100), 
      db: Session = Depends(get_db),
      ):
    organizations = get_organizations(db, skip=skip, limit=limit)
    return organizations
