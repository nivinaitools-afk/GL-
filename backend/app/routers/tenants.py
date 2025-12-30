from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.config import get_db
from ..database.models import Tenant as TenantModel
from ..schemas.tenant import Tenant, TenantCreate

router = APIRouter(prefix="/tenants", tags=["tenants"])

@router.post("", response_model=Tenant)
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    """Create a new tenant (university)."""
    
    db_tenant = TenantModel(**tenant.model_dump())
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

@router.get("/{tenant_id}", response_model=Tenant)
def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    """Get tenant configuration."""
    
    tenant = db.query(TenantModel).filter(TenantModel.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant
