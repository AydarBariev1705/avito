# routers/bids.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from schemas import BidCreate, Bid, BidUpdate
from crud import (get_user_by_username,
                  is_user_responsible_for_org, 
                  create_bid, 
                  get_bids_for_tender, 
                  get_my_bids, 
                  update_bid, 
                  rollback_bid, 
                  get_bid, 
                  is_author_of_tender
                  )
from database import get_db
from enums import DecisionType, BidStatus


router = APIRouter(
    prefix="/api/bids",
    tags=["bids"],
)

@router.post(
        "/new", 
        response_model=Bid, 
        status_code=status.HTTP_201_CREATED,
        )
def endpoint_create_bid(
    bid: BidCreate, 
    db: Session = Depends(get_db),
    ):
    user = get_user_by_username(
        db=db,
        username = bid.creator_username,
        )
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Пользователь не найден",
            )
    

    is_responsible = is_user_responsible_for_org(
        db=db, 
        user_id=user.id, 
        organization_id=bid.organization_id,
        )
    if not is_responsible and not is_author_of_tender(
        db=db, 
        tender_id=bid.tender_id, 
        user_id=user.id,
        ):
        raise HTTPException(
            status_code=403, 
            detail="Нет прав на создание предложения",
            )
    
    new_bid = create_bid(
        db=db,
        bid=bid,
        )
    return new_bid

@router.get(
        "/my", 
        response_model=List[Bid],
        )
def endpoint_list_my_bids(
    username: str,
      db: Session = Depends(get_db),
      ):
    bids = get_my_bids(
        db=db, 
        username=username,
        )
    return bids

@router.get(
        "/{tender_id}/list",
         response_model=List[Bid],
         )
def endpoint_list_bids_for_tender(
    tender_id: int, 
    db: Session = Depends(get_db),
    ):
    bids = get_bids_for_tender(
        db=db, 
        tender_id=tender_id,
        )
    return bids

@router.patch(
        "/{bid_id}/edit", 
        response_model=Bid,
        )
def endpoint_edit_bid(
    bid_id: int, 
    bid: BidUpdate, 
    db: Session = Depends(get_db),
    ):
    db_bid = get_bid(
        db=db, 
        bid_id=bid_id,
        )
    if not db_bid:
        raise HTTPException(
            status_code=404, 
            detail="Предложение не найдено",
            )
    
    
    user = get_user_by_username(
        db=db, 
        username=bid.username,
        )
    if not user or not (is_user_responsible_for_org(
        db=db, 
        user_id=user.id, 
        organization_id=db_bid.organization_id,
        ) or db_bid.creator_id == user.id):
        raise HTTPException(
            status_code=403, 
            detail="Нет доступа к редактированию предложения",
            )
    
    updated_bid = update_bid(
        db=db, 
        db_bid=db_bid, 
        bid=bid,
        )
    return updated_bid

@router.put(
        "/{bid_id}/rollback/{version}",
         response_model=Bid,
         )
def endpoint_rollback_bid(
    bid_id: int, 
    version: int, 
    db: Session = Depends(get_db),
    ):
    db_bid = get_bid(
        db=db, 
        bid_id=bid_id,
        )
    if not db_bid:
        raise HTTPException(
            status_code=404, 
            detail="Предложение не найдено",
            )
    
    rolled_back_bid = rollback_bid(
        db=db, 
        db_bid=db_bid, 
        version=version,
        )
    if not rolled_back_bid:
        raise HTTPException(
            status_code=400, 
            detail="Некорректная версия для отката",
            )
    
    return rolled_back_bid

@router.post(
        "/{bid_id}/decision", 
        response_model=Bid,
        )
def endpoint_bid_decision(
        bid_id: int, 
        username: str, 
        decision: DecisionType, 
        db: Session = Depends(get_db),
        ):
    bid = get_bid(
        db=db, 
        bid_id=bid_id,
        )
    if not bid:
        raise HTTPException(
            status_code=404, 
            detail="Предложение не найдено",
            )
    if bid.status == BidStatus.PUBLISHED:
        return JSONResponse(
            status_code=200, 
            content={
                "message": "Предложение уже опубликовано",
                },
            )

    user = get_user_by_username(
        db=db, 
        username=username,
        )
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Пользователь не найден",
            )
    if not is_user_responsible_for_org(
        db=db, 
        user_id=user.id, 
        organization_id=bid.organization_id,
        ):
        raise HTTPException(
            status_code=403, 
            detail="Нет доступа к редактированию предложения",
            )
    if username not in bid.approved_by:
        if decision == DecisionType.REJECT:
            bid.status = BidStatus.CANCELED
            db.commit()
            return JSONResponse(
                status_code=200, 
                content={
                    "message": "Предложение отклонено",
                    },
                    ) 
        bid.approve_decision_count += 1
        bid.approved_by = bid.approved_by + [username]
        
        db.commit()
        db.refresh(bid)
        
    else:
        raise HTTPException(
            status_code=400, 
            detail="Пользователь уже принял предложение",
            )
        
    if bid.approve_decision_count >=3:
        bid.status = BidStatus.PUBLISHED
        
        db.commit()
        return JSONResponse(
            status_code=200, 
            content={
                "message": "Предложение опубликовано",
                },
                )

    return JSONResponse(
        status_code=200,
          content={
              "message": f"Предложение не опубликовано. До подтверждения осталось: {3 - bid.approve_decision_count} принятия предложения.",
              },
              )


@router.post("/{bid_id}/approved_by")
def endpoint_test(
    bid_id: int,
    db: Session = Depends(get_db),
    ):
    bid = get_bid(
        db=db, 
        bid_id=bid_id,
        )
    if not bid:
        raise HTTPException(
            status_code=404, 
            detail="Предложение не найдено",
            )
    return {"approved_by": bid.approved_by}
