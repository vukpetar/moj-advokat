from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.item_points import (
    crud as ItemPointCrud,
    schemas as ItemPointSchemas
)
from models.user.auth import (
    get_current_active_user,
)
from models.user.schemas import User
from database import get_db

router = APIRouter(
    prefix="/item_points",
    tags=["item_points"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ItemPointSchemas.ItemPoint)
def create_item(item: ItemPointSchemas.ItemPointCreate, db: Session = Depends(get_db)):

    return ItemPointCrud.create_item_point(db=db, item=item)

@router.get("/", response_model=list[ItemPointSchemas.ItemPoint])
def read_item_points(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    item_points = ItemPointCrud.get_item_points(db, skip=skip, limit=limit)
    return item_points

@router.get("/{item_point_id}", response_model=ItemPointSchemas.ItemPoint)
def read_item(
    item_point_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    db_item = ItemPointCrud.get_item_point(db, item_point_id=item_point_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_item