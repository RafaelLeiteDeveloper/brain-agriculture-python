from sqlalchemy import select
from sqlalchemy.sql import func
from app.models import Farmer
from app.models import Crop
from app.validations.farmer import FarmerCreate, FarmerUpdate
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import BrazilianState

state_mapping = {
    "Acre": "Acre",
    "Alagoas": "Alagoas",
    "Amapá": "Amapa",
    "Amazonas": "Amazonas",
    "Bahia": "Bahia",
    "Ceará": "Ceara",
    "Distrito Federal": "DistritoFederal",
    "Espírito Santo": "EspiritoSanto",
    "Goiás": "Goias",
    "Maranhão": "Maranhao",
    "Mato Grosso": "MatoGrosso",
    "Mato Grosso do Sul": "MatoGrossoDoSul",
    "Minas Gerais": "MinasGerais",
    "Pará": "Para",
    "Paraíba": "Paraiba",
    "Paraná": "Parana",
    "Pernambuco": "Pernambuco",
    "Piauí": "Piaui",
    "Rio de Janeiro": "RioDeJaneiro",
    "Rio Grande do Norte": "RioGrandeDoNorte",
    "Rio Grande do Sul": "RioGrandeDoSul",
    "Rondônia": "Rondonia",
    "Roraima": "Roraima",
    "Santa Catarina": "SantaCatarina",
    "São Paulo": "SaoPaulo",
    "Sergipe": "Sergipe",
    "Tocantins": "Tocantins"
}

async def farmer_exists_by_cpf_or_cnpj(db: AsyncSession, farmer_key: str):
    result = await db.execute(select(Farmer).filter((Farmer.cpf == farmer_key) | (Farmer.cnpj == farmer_key)))
    return result.scalars().first() is not None

async def get_farmer(db: AsyncSession, farmer_id: int):
    result = await db.execute(select(Farmer).filter(Farmer.id == farmer_id).options(selectinload(Farmer.crops)))
    return result.scalars().first()

async def get_farmers(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Farmer).offset(skip).limit(limit).options(selectinload(Farmer.crops)))
    return result.scalars().all()

async def create_farmer(db: AsyncSession, farmer: FarmerCreate):
    if farmer.totalVegetationArea + farmer.totalArableArea > farmer.totalFarmArea:
        return "Farm size can't be smaller than vegetation and arable area."
    
    state_enum_value = state_mapping.get(farmer.state)
    if not state_enum_value:
        raise ValueError(f"Invalid state: {farmer.state}")

    db_farmer = Farmer(
        farmerName=farmer.farmerName,
        farmName=farmer.farmName,
        city=farmer.city,
        state=BrazilianState[state_enum_value],
        totalFarmArea=farmer.totalFarmArea,
        totalArableArea=farmer.totalArableArea,
        totalVegetationArea=farmer.totalVegetationArea,
        cpf=farmer.cpf,
        cnpj=farmer.cnpj
    )
    db.add(db_farmer)
    await db.commit()
    await db.refresh(db_farmer)
    
    for crop_name in farmer.crops:
        result = await db.execute(select(Crop).filter(Crop.name == crop_name))
        crop = result.scalars().first()
        if not crop:
            crop = Crop(name=crop_name, farmerId=db_farmer.id)
            db.add(crop)
            await db.commit()
            await db.refresh(crop)
    
    return db_farmer

async def update_farmer(db: AsyncSession, farmer_id: int, farmer: FarmerUpdate):
    db_farmer = await get_farmer(db, farmer_id)
    if db_farmer:
        if farmer.state is not None:
            state_enum_value = state_mapping.get(farmer.state)
            if not state_enum_value:
                raise ValueError(f"Invalid state: {farmer.state}")
        db_farmer.state = state_enum_value
        del farmer.state
        for var, value in vars(farmer).items():
            setattr(db_farmer, var, value) if value else None
        await db.commit()
        await db.refresh(db_farmer)
    return db_farmer

async def delete_farmer(db: AsyncSession, farmer_id: int):
    db_farmer = await get_farmer(db, farmer_id)
    if db_farmer:
        await db.delete(db_farmer)
        await db.commit()
    return None

async def get_dashboard_data(db: AsyncSession):
    total_farmers = (await db.execute(select(func.count(Farmer.id)))).scalar()
    total_crops = (await db.execute(select(func.count(Crop.id)))).scalar()
    total_farm_area = (await db.execute(select(func.sum(Farmer.totalFarmArea)))).scalar()
    total_arable_area = (await db.execute(select(func.sum(Farmer.totalArableArea)))).scalar()
    total_vegetation_area = (await db.execute(select(func.sum(Farmer.totalVegetationArea)))).scalar()
    
    return {
        "total_farmers": total_farmers,
        "total_crops": total_crops,
        "total_farm_area": total_farm_area,
        "total_arable_area": total_arable_area,
        "total_vegetation_area": total_vegetation_area
    }