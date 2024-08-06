from typing import List
from fastapi.responses import JSONResponse
from app.validations.post import validate_farmer_data
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.farmer import get_farmer, farmer_exists_by_cpf_or_cnpj, get_farmers, create_farmer, update_farmer, delete_farmer, get_dashboard_data
from app.validations.farmer import Farmer, FarmerCreate, FarmerUpdate
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=Farmer)
async def create_farmer_endpoint(farmer: FarmerCreate, db: AsyncSession = Depends(get_db)):
    try:
        farmer_key = farmer.cpf if farmer.cpf else farmer.cnpj
        if await farmer_exists_by_cpf_or_cnpj(db=db, farmer_key=farmer_key):
            raise HTTPException(status_code=400, detail="Farmer with this CPF or CNPJ already exists.")
        
        validate_farmer_data(farmer)
        await create_farmer(db, farmer)
        return JSONResponse(content={"message": "Farmer saved successfully"}, status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{farmer_id}", response_model=Farmer)
async def read_farmer(farmer_id: int, db: AsyncSession  = Depends(get_db)):
    db_farmer = await get_farmer(db, farmer_id)
    if db_farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return db_farmer

@router.get("/", response_model=List[Farmer])
async def read_farmers(skip: int = 0, limit: int = 10, db: AsyncSession  = Depends(get_db)):
    farmers = await get_farmers(db, skip=skip, limit=limit)
    return farmers

@router.put("/{farmer_id}")
async def update_farmer_endpoint(farmer_id: int, farmer: FarmerUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_farmer = await update_farmer(db, farmer_id, farmer)
        if not updated_farmer:
            raise HTTPException(status_code=404, detail="Farmer not found")
        return updated_farmer
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{farmer_id}")
async def delete_farmer_endpoint(farmer_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await delete_farmer(db, farmer_id)
        return {"message": "Farmer deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dashboard/data")
async def dashboard_data(db: AsyncSession = Depends(get_db)):
    data = await get_dashboard_data(db)
    return data