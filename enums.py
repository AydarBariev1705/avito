import enum

class TenderStatus(str, enum.Enum):
    CREATED = "CREATED"
    PUBLISHED = "PUBLISHED"
    CLOSED = "CLOSED"

class BidStatus(str, enum.Enum):
    CREATED = "CREATED"
    PUBLISHED = "PUBLISHED"
    CANCELED = "CANCELED"

class OrganizationType(str, enum.Enum):
    IE ='IE'
    LLC = 'LLC'
    JSC = 'JSC'

class DecisionType(str, enum.Enum):
    APPROVE = "approve" 
    REJECT = "reject"

