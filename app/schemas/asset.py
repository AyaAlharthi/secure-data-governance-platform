from enum import Enum

from pydantic import BaseModel


class DataClassification(str, Enum):
    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"


class DataAssetCreate(BaseModel):
    name: str
    owner: str
    department: str
    classification: DataClassification


class DataAssetUpdate(BaseModel):
    name: str | None = None
    owner: str | None = None
    department: str | None = None
    classification: DataClassification | None = None
