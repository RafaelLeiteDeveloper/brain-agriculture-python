from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class BrazilianState(enum.Enum):
    Acre = "Acre"
    Alagoas = "Alagoas"
    Amapa = "Amapá"
    Amazonas = "Amazonas"
    Bahia = "Bahia"
    Ceara = "Ceará"
    DistritoFederal = "Distrito Federal"
    EspiritoSanto = "Espírito Santo"
    Goias = "Goiás"
    Maranhao = "Maranhão"
    MatoGrosso = "Mato Grosso"
    MatoGrossoDoSul = "Mato Grosso do Sul"
    MinasGerais = "Minas Gerais"
    Para = "Pará"
    Paraiba = "Paraíba"
    Parana = "Paraná"
    Pernambuco = "Pernambuco"
    Piaui = "Piauí"
    RioDeJaneiro = "Rio de Janeiro"
    RioGrandeDoNorte = "Rio Grande do Norte"
    RioGrandeDoSul = "Rio Grande do Sul"
    Rondonia = "Rondônia"
    Roraima = "Roraima"
    SantaCatarina = "Santa Catarina"
    SaoPaulo = "São Paulo"
    Sergipe = "Sergipe"
    Tocantins = "Tocantins"

class Farmer(Base):
    __tablename__ = 'farmers'

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(11), nullable=True, unique=True)
    cnpj = Column(String(14), nullable=True, unique=True)
    farmerName = Column(String, nullable=False)
    farmName = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(Enum(BrazilianState), nullable=False)
    totalFarmArea = Column(Float, nullable=False)
    totalArableArea = Column(Float, nullable=False)
    totalVegetationArea = Column(Float, nullable=False)
    crops = relationship("Crop", back_populates="farmer")

class Crop(Base):
    __tablename__ = 'crops'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    farmerId = Column(Integer, ForeignKey('farmers.id', ondelete='CASCADE'))
    farmer = relationship("Farmer", back_populates="crops")
