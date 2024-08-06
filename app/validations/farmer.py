from pydantic import BaseModel
from typing import List, Optional
from typing import List

class CropBase(BaseModel):
    name: str

class CropCreate(CropBase):
    pass

class Crop(CropBase):
    id: int

    class Config:
        orm_mode = True

class FarmerBase(BaseModel):
    farmerName: str
    farmName: str
    city: str
    state: str
    totalFarmArea: float
    totalArableArea: float
    totalVegetationArea: float
    cpf: Optional[str] = None
    cnpj: Optional[str] = None

class FarmerUpdate(FarmerBase):
    pass

class FarmerCreate(FarmerBase):
    crops: List[str]

class Farmer(FarmerBase):
    id: int
    crops: List[Crop]

    class Config:
        orm_mode = True