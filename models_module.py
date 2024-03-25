from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Plant(Base):
    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    strain = Column(String, nullable=False)
    measurements = relationship('Measurement', backref='plant', cascade='all, delete-orphan')
    nutrients = relationship('Nutrient', backref='plant', cascade='all, delete-orphan')
    comments = relationship('Comment', backref='plant', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Plant(id='{self.id}', name='{self.name}', strain='{self.strain}')>"

class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    height = Column(Float, nullable=False)
    leaf_count = Column(Integer, nullable=False)
    stem_diameter = Column(Float, nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)

    def __repr__(self):
        return f"<Measurement(id='{self.id}', date='{self.date}', height='{self.height}', leaf_count='{self.leaf_count}', stem_diameter='{self.stem_diameter}')>"

class NutrientType(Base):
    __tablename__ = 'nutrient_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

    def __repr__(self):
        return f"<NutrientType(id='{self.id}', name='{self.name}', description='{self.description}')>"

class Nutrient(Base):
    __tablename__ = 'nutrients'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)
    nutrient_type_id = Column(Integer, ForeignKey('nutrient_types.id'), nullable=False)
    nutrient_type = relationship('NutrientType')

    def __repr__(self):
        return f"<Nutrient(id='{self.id}', date='{self.date}', amount='{self.amount}', nutrient_type='{self.nutrient_type.name}')>"

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    content = Column(String, nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)

    def __repr__(self):
        return f"<Comment(id='{self.id}', date='{self.date}', content='{self.content[:20]}...')>"