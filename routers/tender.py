# routers/tenders.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from schemas import Tender, TenderCreate, TenderUpdate
from crud import (get_user_by_username,
                  is_user_responsible_for_org,
                  create_tender,
                  get_tenders,
                  get_my_tenders, 
                  update_tender,
                  rollback_tender, 
                  get_tender,
                  )
from database import get_db

router = APIRouter(
    prefix="/api/tenders",
    tags=["tenders"],
)

@router.post(
        "/new", 
        response_model=Tender, 
        status_code=status.HTTP_201_CREATED,
        )
def endpoint_create_tender(
    tender: TenderCreate, 
    db: Session = Depends(get_db),
    ):
    user = get_user_by_username(
        db=db,
        username=tender.creator_username,
        )
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Пользователь не найден",
            )
    is_responsible = is_user_responsible_for_org(
        db=db, 
        user_id=user.id, 
        organization_id=tender.organization_id,
        )
    if not is_responsible:
        raise HTTPException(
            status_code=403, 
            detail="Пользователь не является ответственным за организацию",
            )
    
    new_tender = create_tender(
        db=db, 
        tender=tender,
        )
    return new_tender

@router.get("/", 
            response_model=List[Tender],
            )
def endpoint_list_tenders(
    service_type: str = None,
    db: Session = Depends(get_db),
    username: str = None,
    ):
    tenders = get_tenders(
        db=db, 
        service_type=service_type, 
        username=username,
        )
    return tenders

@router.get(
        "/my", 
        response_model=List[Tender],
        )
def endpoint_list_my_tenders(
    username: str, 
    db: Session = Depends(get_db),
    ):
    tenders = get_my_tenders(
        db=db, 
        username=username,
        )
    return tenders

@router.patch(
        "/{tender_id}/edit", 
        response_model=Tender,
        )
def endpoint_edit_tender(
    tender_id: int, 
    tender: TenderUpdate, 
    db: Session = Depends(get_db),
    ):
    db_tender = get_tender(
        db=db, 
        tender_id=tender_id,
        )
    if not db_tender:
        raise HTTPException(
            status_code=404, 
            detail="Тендер не найден",
            )
    
    user = get_user_by_username(
        db=db, 
        username=tender.username,
        )
    if not user or not is_user_responsible_for_org(
        db=db,
        user_id=user.id,
        organization_id=db_tender.organization_id,
        ):
        raise HTTPException(
            status_code=403, 
            detail="Нет доступа к редактированию тендера",
            )
    
    updated_tender = update_tender(
        db=db,
        db_tender=db_tender, 
        tender=tender,
        )
    return updated_tender

@router.put(
        "/{tender_id}/rollback/{version}", 
        response_model=Tender,
        )
def endpoint_rollback_tender(
    tender_id: int, 
    version: int, 
    db: Session = Depends(get_db),
    ):
    db_tender = get_tender(
        db=db, 
        tender_id=tender_id,
        )
    if not db_tender:
        raise HTTPException(
            status_code=404, 
            detail="Тендер не найден",
            )
    
    rolled_back_tender = rollback_tender(
        db=db, 
        db_tender=db_tender, 
        version=version,
        )
    if not rolled_back_tender:
        raise HTTPException(
            status_code=400, 
            detail="Некорректная версия для отката",
            )
    
    return rolled_back_tender