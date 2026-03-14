from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from app.crud import company as crud_company

router = APIRouter()


@router.post(
    "/", 
    response_model=CompanyResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new company",
    description="Create a new company with the provided information."
)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new company with all the information:
    
    - **name**: Company name
    - **corporate_domain**: Corporate email domain
    - **plan**: Subscription plan (basic, professional, enterprise)
    - **status**: Company status (active, inactive, suspended)
    """
    return crud_company.create_company(db=db, company=company)


@router.get(
    "/",
    response_model=List[CompanyResponse],
    summary="List all companies",
    description="Retrieve a list of all companies with pagination."
)
def list_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all companies with pagination support.
    """
    companies = crud_company.get_companies(db, skip=skip, limit=limit)
    return companies


@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
    summary="Get company by ID",
    description="Retrieve a specific company by its ID."
)
def get_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific company by ID.
    """
    db_company = crud_company.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    return db_company


@router.put(
    "/{company_id}",
    response_model=CompanyResponse,
    summary="Update company",
    description="Update an existing company's information."
)
def update_company(
    company_id: int,
    company: CompanyUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a company's information.
    """
    db_company = crud_company.update_company(db, company_id=company_id, company=company)
    if db_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    return db_company


@router.delete(
    "/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete company",
    description="Delete a company by its ID."
)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a company.
    """
    success = crud_company.delete_company(db, company_id=company_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    return None
