from .utils import is_valid_cnpj, is_valid_cpf
from typing import List
from app.validations.farmer import FarmerCreate

def validate_farmer_data(farmer: FarmerCreate):
    if farmer.totalArableArea > farmer.totalFarmArea:
        raise ValueError("totalArableArea cannot be greater than totalFarmArea.")
    if farmer.totalVegetationArea > farmer.totalFarmArea:
        raise ValueError("totalVegetationArea cannot be greater than totalFarmArea.")
    if farmer.totalArableArea + farmer.totalVegetationArea > farmer.totalFarmArea:
        raise ValueError("totalVegetationArea + totalArableArea cannot be greater than totalFarmArea.")
    if not farmer.cpf and not farmer.cnpj:
        raise ValueError("Either CPF or CNPJ must be provided.")
    if farmer.cpf and farmer.cnpj:
        raise ValueError("Only one of CPF or CNPJ should be provided.")
    if farmer.cpf and not is_valid_cpf(farmer.cpf):
        raise ValueError("Invalid CPF.")
    if farmer.cnpj and not is_valid_cnpj(farmer.cnpj):
        raise ValueError("Invalid CNPJ.")
