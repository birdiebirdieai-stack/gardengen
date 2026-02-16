from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..database import get_db
from ..models import Association, Vegetable
from ..schemas import AssociationCreate, AssociationOut, AssociationWithNames

router = APIRouter(prefix="/api/associations", tags=["associations"])


@router.get("", response_model=list[AssociationWithNames])
def list_associations(db: Session = Depends(get_db)):
    rows = db.query(Association).all()
    result = []
    for a in rows:
        main = db.get(Vegetable, a.vegetable_id_main)
        target = db.get(Vegetable, a.vegetable_id_target)
        result.append(AssociationWithNames(
            vegetable_id_main=a.vegetable_id_main,
            vegetable_id_target=a.vegetable_id_target,
            score=a.score,
            reason=a.reason,
            main_name=main.name if main else "",
            target_name=target.name if target else "",
        ))
    return result


@router.get("/{vegetable_id}", response_model=list[AssociationWithNames])
def get_associations_for(vegetable_id: int, db: Session = Depends(get_db)):
    rows = db.query(Association).filter(
        or_(
            Association.vegetable_id_main == vegetable_id,
            Association.vegetable_id_target == vegetable_id,
        )
    ).all()
    result = []
    for a in rows:
        main = db.get(Vegetable, a.vegetable_id_main)
        target = db.get(Vegetable, a.vegetable_id_target)
        result.append(AssociationWithNames(
            vegetable_id_main=a.vegetable_id_main,
            vegetable_id_target=a.vegetable_id_target,
            score=a.score,
            reason=a.reason,
            main_name=main.name if main else "",
            target_name=target.name if target else "",
        ))
    return result


@router.post("", response_model=AssociationOut, status_code=201)
def upsert_association(data: AssociationCreate, db: Session = Depends(get_db)):
    existing = db.query(Association).filter_by(
        vegetable_id_main=data.vegetable_id_main,
        vegetable_id_target=data.vegetable_id_target,
    ).first()
    if existing:
        existing.score = data.score
        existing.reason = data.reason
    else:
        existing = Association(**data.model_dump())
        db.add(existing)
    # also upsert reverse
    reverse = db.query(Association).filter_by(
        vegetable_id_main=data.vegetable_id_target,
        vegetable_id_target=data.vegetable_id_main,
    ).first()
    if reverse:
        reverse.score = data.score
        reverse.reason = data.reason
    else:
        db.add(Association(
            vegetable_id_main=data.vegetable_id_target,
            vegetable_id_target=data.vegetable_id_main,
            score=data.score,
            reason=data.reason,
        ))
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{main_id}/{target_id}", status_code=204)
def delete_association(main_id: int, target_id: int, db: Session = Depends(get_db)):
    a = db.query(Association).filter_by(
        vegetable_id_main=main_id, vegetable_id_target=target_id
    ).first()
    if a:
        db.delete(a)
    # also delete reverse
    r = db.query(Association).filter_by(
        vegetable_id_main=target_id, vegetable_id_target=main_id
    ).first()
    if r:
        db.delete(r)
    db.commit()
