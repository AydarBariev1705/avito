from sqlalchemy.orm import Session
from models import  Employee, Organization, OrganizationResponsible
from enums import OrganizationType


def create_initial_data(db: Session):
    
    if db.query(Employee).count() > 0 or db.query(Organization).count() > 0:
        return

    
    employees = [
        Employee(
            username="johndoe",
              first_name="John", 
              last_name="Doe",
              ),
        Employee(
            username="janedoe", 
            first_name="Jane", 
            last_name="Doe",
            ),
        Employee(
            username="alice", 
            first_name="Alice", 
            last_name="Smith",
            ),
        Employee(
            username="john", 
            first_name="John", 
            last_name="Doe",
            ),
        Employee(
            username="jane", 
            first_name="Jane", 
            last_name="Doe",
            ),
        Employee(
            username="alicesmith",
              first_name="Alice", 
              last_name="Smith",
              ),
        Employee(
            username="travis", 
            first_name="Travis", 
            last_name="Doe",
            ),
        Employee(
            username="bob0", 
            first_name="Bob", 
            last_name="Doe",
            ),
        Employee(
            username="sam", 
            first_name="Sam", 
            last_name="Smith",
            ),
    ]
    db.add_all(employees)
    db.commit()  

    
    organizations = [
        Organization(
            name="TechCorp", 
            description="IT company", 
            type=OrganizationType.IE,
            ),
        Organization(
            name="HealthInc", 
            description="Healthcare services", 
            type=OrganizationType.JSC,
            ),
        Organization(
            name="EduLtd", 
            description="Education services", 
            type=OrganizationType.LLC,
            ),
    ]
    db.add_all(organizations)
    db.commit()  

    
    employees = db.query(Employee).all()
    organizations = db.query(Organization).all()

    
    organization_responsibles = [
        OrganizationResponsible(
            organization_id=organizations[0].id, 
            user_id=employees[0].id),
        OrganizationResponsible(
            organization_id=organizations[2].id, 
            user_id=employees[1].id),
        OrganizationResponsible(
            organization_id=organizations[1].id, 
            user_id=employees[2].id),
        OrganizationResponsible(
            organization_id=organizations[0].id, 
            user_id=employees[3].id),
        OrganizationResponsible(
            organization_id=organizations[2].id, 
            user_id=employees[4].id),
        OrganizationResponsible(
            organization_id=organizations[1].id, 
            user_id=employees[5].id),
        OrganizationResponsible(
            organization_id=organizations[0].id, 
            user_id=employees[6].id),
        OrganizationResponsible(
            organization_id=organizations[2].id, 
            user_id=employees[7].id),
        OrganizationResponsible(
            organization_id=organizations[1].id, 
            user_id=employees[8].id),
    ]
    db.add_all(organization_responsibles)
    db.commit()
