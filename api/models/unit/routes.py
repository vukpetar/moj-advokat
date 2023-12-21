from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.unit import (
    crud as unitCrud,
    schemas as unitSchemas
)
from models.user.auth import (
    get_current_active_user,
)
from models.user.schemas import User
from database import get_db

router = APIRouter(
    prefix="/units",
    tags=["units"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=unitSchemas.Unit)
async def create_unit(unit: unitSchemas.UnitCreate, db: Session = Depends(get_db)):

    return unitCrud.create_unit(db=db, unit=unit)

@router.get("/", response_model=list[unitSchemas.Unit])
async def read_units(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    units = unitCrud.get_units(db, skip=skip, limit=limit)
    return units

@router.get("/{unit_id}", response_model=unitSchemas.Unit)
async def read_unit(
    unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    db_unit = unitCrud.get_unit(db, unit_id=unit_id)
    if db_unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return db_unit