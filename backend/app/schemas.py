from pydantic import BaseModel


# ---------- Vegetable ----------
class VegetableBase(BaseModel):
    name: str
    variety: str = ""
    slug: str
    grid_width: int
    grid_height: int
    color: str = "#22c55e"


class VegetableCreate(VegetableBase):
    pass


class VegetableUpdate(BaseModel):
    name: str | None = None
    variety: str | None = None
    slug: str | None = None
    grid_width: int | None = None
    grid_height: int | None = None
    color: str | None = None


class VegetableOut(VegetableBase):
    id: int
    model_config = {"from_attributes": True}


# ---------- Association ----------
class AssociationBase(BaseModel):
    vegetable_id_main: int
    vegetable_id_target: int
    score: int
    reason: str = ""


class AssociationCreate(AssociationBase):
    pass


class AssociationOut(AssociationBase):
    model_config = {"from_attributes": True}


class AssociationWithNames(AssociationOut):
    main_name: str = ""
    target_name: str = ""


# ---------- Generate ----------
class GenerateItem(BaseModel):
    vegetable_id: int
    quantity: int


class GenerateRequest(BaseModel):
    width_cm: int
    height_cm: int
    items: list[GenerateItem]


class PlacedVegetable(BaseModel):
    vegetable_id: int
    x: int
    y: int
    w: int
    h: int


class GenerateResponse(BaseModel):
    placed: list[PlacedVegetable]
    rejected: list[int]  # vegetable_ids that couldn't be placed
    global_score: float
