from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Farmer(Base):
    __tablename__ = 'farmers'
    
    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, nullable=True)
    cnpj = Column(String, nullable=True)
    farmerName = Column(String, nullable=False)
    farmName = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    totalFarmArea = Column(Float, nullable=False)
    totalArableArea = Column(Float, nullable=False)
    totalVegetationArea = Column(Float, nullable=False)
    
    crops = relationship("Crop", back_populates="farmer", cascade="all, delete")
