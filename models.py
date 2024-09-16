from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base
from enums import TenderStatus, BidStatus, OrganizationType
import datetime



class Tender(Base):
    __tablename__ = "tenders"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        )
    name = Column(
        String(100), 
        index=True,
        )
    description = Column(String(1000))
    service_type = Column(String(100))
    status = Column(
        Enum(TenderStatus), 
        default=TenderStatus.CREATED,
        )
    organization_id = Column(
        Integer, 
        ForeignKey("organization.id"),
        )
    created_at = Column(
        DateTime, 
        default=datetime.datetime.utcnow,
        )
    updated_at = Column(
        DateTime, 
        default=datetime.datetime.utcnow, 
        onupdate=datetime.datetime.utcnow,)
    version = Column(
        Integer, 
        default=1,
        )

    organization = relationship(
        "Organization", 
        back_populates="tenders",
        )
    bids = relationship(
        "Bid", 
        back_populates="tender",
        )
    histories = relationship(
        "TenderHistory", 
        back_populates="tender",
        )

class Bid(Base):
    __tablename__ = "bids"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        )
    name = Column(
        String(100),
         index=True,
         )
    description = Column(String(1000))
    status = Column(
        Enum(BidStatus), 
        default=BidStatus.CREATED,
        )
    tender_id = Column(
        Integer, 
        ForeignKey("tenders.id"),
        )
    organization_id = Column(
        Integer, 
        ForeignKey("organization.id"),
        )
    created_at = Column(
        DateTime, 
        default=datetime.datetime.utcnow,
        )
    updated_at = Column(
        DateTime, 
        default=datetime.datetime.utcnow, 
        onupdate=datetime.datetime.utcnow,
        )
    version = Column(
        Integer, 
        default=1,
        )
    creator_id = Column(
        Integer, 
        ForeignKey("employee.id"),
        )
    approve_decision_count = Column(
        Integer, 
        default=0,
        )
    approved_by = Column(
        ARRAY(String),
         default=[],
         )

    tender = relationship(
        "Tender", 
        back_populates="bids",
        )
    organization = relationship(
        "Organization", 
        back_populates="bids",
        )
    creator = relationship(
        "Employee", 
        back_populates="bids",
        )
    histories = relationship(
        "BidHistory", 
        back_populates="bid",
        )
    
    

class Employee(Base):
    __tablename__ = "employee"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        )
    username = Column(
        String(50),
         unique=True, 
         nullable=False,
         )
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(
        DateTime, 
        default=datetime.datetime.utcnow,
        )
    updated_at = Column(
        DateTime, 
        default=datetime.datetime.utcnow, 
        onupdate=datetime.datetime.utcnow,
        )

    bids = relationship(
        "Bid",
         back_populates="creator",
         )
    responsibilities = relationship(
        "OrganizationResponsible",
          back_populates="user",
          )

class Organization(Base):
    __tablename__ = "organization"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        )
    name = Column(
        String(100),
         nullable=False,
         )
    description = Column(String)
    type = Column(
        Enum(OrganizationType),
        nullable=False,
        )
    created_at = Column(
        DateTime, 
        default=datetime.datetime.utcnow,
        )
    updated_at = Column(
        DateTime, 
        default=datetime.datetime.utcnow, 
        onupdate=datetime.datetime.utcnow,
        )

    tenders = relationship(
        "Tender", 
        back_populates="organization",
        )
    bids = relationship(
        "Bid", 
        back_populates="organization",
        )
    responsible = relationship(
        "OrganizationResponsible", 
        back_populates="organization",
        )

class OrganizationResponsible(Base):
    __tablename__ = "organization_responsible"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        )
    organization_id = Column(
        Integer, 
        ForeignKey(
            "organization.id", 
            ondelete="CASCADE",
            ),
        )
    user_id = Column(
        Integer, 
        ForeignKey(
            "employee.id", 
            ondelete="CASCADE",
            ),
            )

    organization = relationship(
        "Organization", 
        back_populates="responsible",
        )
    user = relationship(
        "Employee", 
        back_populates="responsibilities",
        )

class TenderHistory(Base):
    __tablename__ = "tender_history"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        )
    tender_id = Column(
        Integer, 
        ForeignKey("tenders.id"),
        )
    name = Column(String(100))
    description = Column(String(1000))
    status = Column(Enum(TenderStatus))
    version = Column(Integer)
    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow),
    
    service_type = Column(String(100))

    tender = relationship("Tender", back_populates="histories")

class BidHistory(Base):
    __tablename__ = "bid_history"

    id = Column(
        Integer,
         primary_key=True,
        index=True,
        )
    bid_id = Column(
        Integer,
          ForeignKey("bids.id"),
          )
    name = Column(String(100))
    description = Column(String(1000))
    status = Column(Enum(BidStatus))
    version = Column(Integer)
    timestamp = Column(
        DateTime,
         default=datetime.datetime.utcnow,
         )

    bid = relationship(
        "Bid",
         back_populates="histories",
         )

