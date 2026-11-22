from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.asset import DataAssetCreate, DataAssetUpdate
from app.services.asset_service import (
    create_asset,
    get_assets,
    get_asset_by_id,
    update_asset,
    delete_asset
)

router = APIRouter()


@router.post("/assets")
def add_asset(
    asset: DataAssetCreate,
    db: Session = Depends(get_db)
):
    return create_asset(db, asset)


@router.get("/assets")
def list_assets(db: Session = Depends(get_db)):
    return get_assets(db)


@router.get("/assets/{asset_id}")
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = get_asset_by_id(db, asset_id)

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    return asset


@router.put("/assets/{asset_id}")
def edit_asset(
    asset_id: int,
    asset_data: DataAssetUpdate,
    db: Session = Depends(get_db)
):
    asset = update_asset(db, asset_id, asset_data)

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    return {
        "message": "Asset updated successfully",
        "asset": asset
    }


@router.delete("/assets/{asset_id}")
def remove_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = delete_asset(db, asset_id)

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    return {
        "message": "Asset deleted successfully",
        "asset_id": asset_id
    }
