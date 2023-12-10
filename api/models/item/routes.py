from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.item import (
    crud as itemCrud,
    schemas as itemSchemas
)
from models.user.auth import (
    get_current_active_user,
)
from models.user.schemas import User
from database import get_db

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=itemSchemas.Item)
def create_item(item: itemSchemas.ItemCreate, db: Session = Depends(get_db)):

    return itemCrud.create_item(db=db, item=item)

@router.get("/", response_model=list[itemSchemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    items = itemCrud.get_items(db, skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=itemSchemas.Item)
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    db_item = itemCrud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item