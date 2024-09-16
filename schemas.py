from pydantic import BaseModel, Field
from typing import Optional
from enums import TenderStatus, BidStatus, DecisionType



# Schemas for Tender
class TenderBase(BaseModel):
    name: str = Field(..., max_length=100)
    service_type: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=1000)


class TenderCreate(TenderBase):
    organization_id: int
    creator_username: str

class TenderUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    service_type: Optional[str] = Field(None, max_length=100)
    status: Optional[TenderStatus] = None
    organization_id: Optional[int] = None
    username: str

class Tender(TenderBase):
    id: int
    status: TenderStatus
    version: int
    organization_id: int

    class Config:
        orm_mode = True

# Schemas for Bid
class BidBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=1000)

class BidCreate(BidBase):
    tender_id: int
    organization_id: int
    creator_username: str

class BidUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[BidStatus] = Field(None)
    tender_id: Optional[int] = Field(None)
    organization_id: Optional[int] = Field(None)
    username: str

class Bid(BidBase):
    id: int
    status: BidStatus
    version: int
    tender_id: int
    organization_id: int
    creator_id: int

    class Config:
        orm_mode = True

# Schema for BidDecision
class BidDecision(BaseModel):
    bid_id: int
    decision: DecisionType 
    decision_maker_username: str
    organization_id: int


class TenderHistoryBase(BaseModel):
    name: str
    description: Optional[str]
    status: TenderStatus
    version: int
    service_type: str = Field(..., max_length=100)

    class Config:
        orm_mode = True

class BidHistoryBase(BaseModel):
    name: str
    description: Optional[str]
    status: BidStatus
    version: int

    class Config:
        orm_mode = True

class EmployeeBase(BaseModel):
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


    class Config:
        orm_mode = True
        

class OrganizationBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    type: str


    class Config:
        orm_mode = True



