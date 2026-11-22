from sqlalchemy.orm import Session

from app.models.asset import DataAsset
from app.schemas.asset import DataAssetCreate, DataAssetUpdate


def create_asset(db: Session, asset: DataAssetCreate):
    db_asset = DataAsset(**asset.model_dump())

    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)

    return {
        "message": "Asset created successfully",
        "asset": {
            "id": db_asset.id,
            "name": db_asset.name,
            "owner": db_asset.owner,
            "department": db_asset.department,
            "classification": db_asset.classification
        }
    }


def get_assets(db: Session):
    return db.query(DataAsset).all()


def get_asset_by_id(db: Session, asset_id: int):
    return db.query(DataAsset).filter(DataAsset.id == asset_id).first()


def update_asset(db: Session, asset_id: int, asset_data: DataAssetUpdate):
    db_asset = get_asset_by_id(db, asset_id)

    if db_asset is None:
        return None

    update_data = asset_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_asset, field, value)

    db.commit()
    db.refresh(db_asset)

    return db_asset


def delete_asset(db: Session, asset_id: int):
    db_asset = get_asset_by_id(db, asset_id)

    if db_asset is None:
        return None

    db.delete(db_asset)
    db.commit()

    return db_asset
