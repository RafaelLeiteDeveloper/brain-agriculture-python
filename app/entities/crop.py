from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Crop(Base):
    __tablename__ = 'crops'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    farmer_id = Column(Integer, ForeignKey('farmers.id'))
    
    farmer = relationship("Farmer", back_populates="crops")