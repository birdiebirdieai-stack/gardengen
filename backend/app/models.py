from sqlalchemy import Column, Integer, String, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Vegetable(Base):
    __tablename__ = "vegetables"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    variety = Column(String, default="")
    slug = Column(String, unique=True, nullable=False)
    grid_width = Column(Integer, nullable=False)   # in 5cm cells
    grid_height = Column(Integer, nullable=False)  # in 5cm cells
    color = Column(String, nullable=False, default="#22c55e")


class Association(Base):
    __tablename__ = "associations"
    __table_args__ = (
        PrimaryKeyConstraint("vegetable_id_main", "vegetable_id_target"),
    )

    vegetable_id_main = Column(Integer, ForeignKey("vegetables.id"), nullable=False)
    vegetable_id_target = Column(Integer, ForeignKey("vegetables.id"), nullable=False)
    score = Column(Integer, nullable=False)  # -50 to +50
    reason = Column(String, default="")

    main = relationship("Vegetable", foreign_keys=[vegetable_id_main])
    target = relationship("Vegetable", foreign_keys=[vegetable_id_target])
