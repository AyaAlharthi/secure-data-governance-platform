from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class DataAsset(Base):
    __tablename__ = "data_assets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(255))

    owner: Mapped[str] = mapped_column(String(255))

    department: Mapped[str] = mapped_column(String(255))

    classification: Mapped[str] = mapped_column(String(100))