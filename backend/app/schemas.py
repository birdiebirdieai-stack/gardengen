from pydantic import BaseModel, Field


# ---------- Vegetable ----------
class VegetableBase(BaseModel):
    name: str = Field(..., max_length=100)
    variety: str = Field("", max_length=100)
    slug: str = Field(..., max_length=100)
    grid_width: int = Field(..., ge=1, le=500)
    grid_height: int = Field(..., ge=1, le=500)
    color: str = Field("#22c55e", max_length=7)


class VegetableCreate(VegetableBase):
    pass


class VegetableUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    variety: str | None = Field(None, max_length=100)
    slug: str | None = Field(None, max_length=100)
    grid_width: int | None = Field(None, ge=1, le=500)
    grid_height: int | None = Field(None, ge=1, le=500)
    color: str | None = Field(None, max_length=7)


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
    quantity: int = Field(..., ge=1, le=1000)


class GenerateRequest(BaseModel):
    width_cm: int = Field(..., ge=10, le=2000)
    height_cm: int = Field(..., ge=10, le=2000)
    items: list[GenerateItem] = Field(..., max_length=50)


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
