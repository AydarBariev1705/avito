from sqlalchemy import or_
from sqlalchemy.orm import Session
from models import (Employee, 
                    OrganizationResponsible, 
                    Tender, 
                    Bid, 
                    TenderHistory, 
                    BidHistory, 
                    Organization,
                    )
from schemas import (TenderUpdate, 
                     TenderCreate, 
                     BidCreate, 
                     BidUpdate,
                     ) 
from enums import BidStatus, TenderStatus

def get_user_by_username(db: Session, username: str):
    return db.query(Employee).filter(Employee.username == username).first()

def is_user_responsible_for_org(db: Session, user_id: int, organization_id: int):
    return db.query(OrganizationResponsible).filter(
        OrganizationResponsible.user_id == user_id,
        OrganizationResponsible.organization_id == organization_id
    ).first() is not None

def is_author_of_tender(db: Session, tender_id: int, user_id: int):
    tender = db.query(Tender).filter(Tender.id == tender_id).first()
    if tender and tender.organization_id:
        responsible_users = db.query(OrganizationResponsible).filter(
            OrganizationResponsible.organization_id == tender.organization_id
        ).all()
        return any(res.user_id == user_id for res in responsible_users)
    return False

def create_tender(db: Session, tender: TenderCreate):
    db_tender = Tender(
        name=tender.name,
        description=tender.description,
        service_type=tender.service_type,
        organization_id=tender.organization_id,
        status=TenderStatus.CREATED,
    )
    db.add(db_tender)
    db.commit()
    db.refresh(db_tender)
    # Сохранение в истории
    save_tender_history(db, db_tender)
    return db_tender

def update_tender(db: Session, db_tender: Tender, tender: TenderUpdate):
    if tender.name:
        db_tender.name = tender.name
    if tender.description:
        db_tender.description = tender.description
    if tender.service_type:
        db_tender.service_type = tender.service_type
    if tender.status:
        db_tender.status = tender.status
    if tender.organization_id:
        db_tender.organization_id = tender.organization_id
    db_tender.version += 1
    db.commit()
    db.refresh(db_tender)
    # Сохранение в истории
    save_tender_history(db, db_tender)
    return db_tender

def rollback_tender(db: Session, db_tender: Tender, version: int):
    history = db.query(TenderHistory).filter(
        TenderHistory.tender_id == db_tender.id,
        TenderHistory.version == version
    ).first()
    if history:
        db_tender.name = history.name
        db_tender.description = history.description
        db_tender.status = history.status
        db_tender.service_type = history.service_type
        db_tender.version += 1
        db.commit()
        db.refresh(db_tender)
        # Сохранение в истории
        save_tender_history(db, db_tender)
        return db_tender
    return None

def save_tender_history(db: Session, tender: Tender):
    history = TenderHistory(
        tender_id=tender.id,
        name=tender.name,
        description=tender.description,
        status=tender.status,
        version=tender.version,
        service_type=tender.service_type
    )
    db.add(history)
    db.commit()

def create_bid(db: Session, bid: BidCreate):
    user = get_user_by_username(db, bid.creator_username)
    if not user:
        raise ValueError("User not found")

    db_bid = Bid(
        name=bid.name,
        description=bid.description,
        tender_id=bid.tender_id,
        organization_id=bid.organization_id,
        status=BidStatus.CREATED,
        creator_id=user.id
    )
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    # Сохранение в истории
    save_bid_history(db, db_bid)
    return db_bid

def update_bid(db: Session, db_bid: Bid, bid: BidUpdate):
    if bid.name:
        db_bid.name = bid.name
    if bid.description:
        db_bid.description = bid.description
    if bid.status:
        db_bid.status = bid.status
    db_bid.version += 1
    db.commit()
    db.refresh(db_bid)
    # Сохранение в истории
    save_bid_history(db, db_bid)
    return db_bid

def rollback_bid(db: Session, db_bid: Bid, version: int):
    history = db.query(BidHistory).filter(
        BidHistory.bid_id == db_bid.id,
        BidHistory.version == version
    ).first()
    if history:
        db_bid.name = history.name
        db_bid.description = history.description
        db_bid.status = history.status
        db_bid.version += 1
        db.commit()
        db.refresh(db_bid)
        # Сохранение в истории
        save_bid_history(db, db_bid)
        return db_bid
    return None

def save_bid_history(db: Session, bid: Bid):
    history = BidHistory(
        bid_id=bid.id,
        name=bid.name,
        description=bid.description,
        status=bid.status,
        version=bid.version,
    )
    db.add(history)
    db.commit()

def get_tenders(db: Session, service_type: str = None, username: str = None):
    if not username:
        # Если username не указан, возвращаем все тендеры со статусом PUBLISHED
        query = db.query(Tender).filter(Tender.status == TenderStatus.PUBLISHED)
        if service_type:
            query = query.filter(Tender.service_type == service_type)
        return query.all()

    # Если username указан, сначала находим организации, к которым прикреплен этот username
    user_organization_ids = db.query(OrganizationResponsible.organization_id).join(
        Employee, Employee.id == OrganizationResponsible.user_id
    ).filter(Employee.username == username).all()

    # Преобразуем результат в список идентификаторов организаций
    organization_ids = [org_id for (org_id,) in user_organization_ids]

    # Формируем запрос для получения тендеров
    query = db.query(Tender).filter(
        or_(
            Tender.status == TenderStatus.PUBLISHED,
            Tender.organization_id.in_(organization_ids)
        )
    )

    if service_type:
        query = query.filter(Tender.service_type == service_type)
    
    return query.all()

def get_organization_id_by_user_id(db: Session, user_id: int) -> int:
    org_responsible = db.query(OrganizationResponsible).filter(OrganizationResponsible.user_id == user_id).first()
    if org_responsible:
        return org_responsible.organization_id
    return None

def get_my_tenders(db: Session, username: str):
    user = get_user_by_username(db, username)
    print(user)
    if not user:
        return []
    org_ids = [res.organization_id for res in db.query(OrganizationResponsible).filter(OrganizationResponsible.user_id == user.id)]
    return db.query(Tender).filter(Tender.organization_id.in_(org_ids)).all()

def get_bids_for_tender(db: Session, tender_id: int):
    return db.query(Bid).filter(Bid.tender_id == tender_id).all()

def get_my_bids(db: Session, username: str):
    user = get_user_by_username(db, username)
    if not user:
        return []
    return db.query(Bid).filter(Bid.creator_id == user.id).all()

def get_bid(db: Session, bid_id: int):
    return db.query(Bid).filter(Bid.id == bid_id).first()


def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Employee).offset(skip).limit(limit).all()

# Организации
def get_organizations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Organization).offset(skip).limit(limit).all()

def get_tender(db: Session, tender_id: int):
    return db.query(Tender).filter(Tender.id == tender_id).first()