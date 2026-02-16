from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Vegetable
from ..schemas import VegetableCreate, VegetableOut, VegetableUpdate

router = APIRouter(prefix="/api/vegetables", tags=["vegetables"])


@router.get("", response_model=list[VegetableOut])
def list_vegetables(search: str = Query("", alias="q"), db: Session = Depends(get_db)):
    q = db.query(Vegetable)
    if search:
        q = q.filter(Vegetable.name.ilike(f"%{search}%"))
    return q.order_by(Vegetable.name).all()


@router.get("/{slug}", response_model=VegetableOut)
def get_vegetable(slug: str, db: Session = Depends(get_db)):
    v = db.query(Vegetable).filter_by(slug=slug).first()
    if not v:
        raise HTTPException(404, "Vegetable not found")
    return v


@router.post("", response_model=VegetableOut, status_code=201)
def create_vegetable(data: VegetableCreate, db: Session = Depends(get_db)):
    v = Vegetable(**data.model_dump())
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


@router.put("/{id}", response_model=VegetableOut)
def update_vegetable(id: int, data: VegetableUpdate, db: Session = Depends(get_db)):
    v = db.get(Vegetable, id)
    if not v:
        raise HTTPException(404, "Vegetable not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(v, key, val)
    db.commit()
    db.refresh(v)
    return v


@router.delete("/{id}", status_code=204)
def delete_vegetable(id: int, db: Session = Depends(get_db)):
    v = db.get(Vegetable, id)
    if not v:
        raise HTTPException(404, "Vegetable not found")
    db.delete(v)
    db.commit()
