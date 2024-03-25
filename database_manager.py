import os

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

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

class DatabaseManager:
    def __init__(self, database_uri):
        self.engine = create_engine(database_uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_session(self):
        return self.Session()

    def add_plant(self, session, name, strain):
        plant = Plant(name=name, strain=strain)
        session.add(plant)
        session.commit()
        return plant

    def get_plant(self, session, plant_id):
        return session.query(Plant).get(plant_id)

    def get_all_plants(self, session):
        return session.query(Plant).all()

    def add_measurement(self, session, plant, date, height, leaf_count, stem_diameter):
        measurement = Measurement(date=date, height=height, leaf_count=leaf_count, stem_diameter=stem_diameter, plant=plant)
        session.add(measurement)
        session.commit()
        return measurement

    def get_measurements(self, session, plant):
        return session.query(Measurement).filter_by(plant=plant).all()

    def add_nutrient_type(self, session, name, description=None):
        nutrient_type = NutrientType(name=name, description=description)
        session.add(nutrient_type)
        session.commit()
        return nutrient_type

    def get_nutrient_type(self, session, nutrient_type_id):
        return session.query(NutrientType).get(nutrient_type_id)

    def get_all_nutrient_types(self, session):
        return session.query(NutrientType).all()

    def add_nutrient(self, session, plant, nutrient_type, date, amount):
        nutrient = Nutrient(date=date, amount=amount, plant=plant, nutrient_type=nutrient_type)
        session.add(nutrient)
        session.commit()
        return nutrient

    def get_nutrients(self, session, plant):
        return session.query(Nutrient).filter_by(plant=plant).all()

    def add_comment(self, session, plant, date, content):
        comment = Comment(date=date, content=content, plant=plant)
        session.add(comment)
        session.commit()
        return comment

    def get_comments(self, session, plant):
        return session.query(Comment).filter_by(plant=plant).all()

if __name__ == '__main__':
    database_uri = os.environ.get('DATABASE_URI', 'sqlite:///plant_tracker.db')
    db_manager = DatabaseManager(database_uri)

    # Example usage
    with db_manager.create_session() as session:
        # Add a new plant
        plant = db_manager.add_plant(session, 'Sour Diesel', 'Hybrid')

        # Add a measurement
        measurement = db_manager.add_measurement(session, plant, date(2023, 5, 1), 25.0, 12, 5.2)

        # Add a nutrient type
        nutrient_type = db_manager.add_nutrient_type(session, 'Terra Vega', 'Vegetative nutrient')

        # Add a nutrient
        nutrient = db_manager.add_nutrient(session, plant, nutrient_type, date(2023, 5, 1), 10.0)

        # Add a comment
        comment = db_manager.add_comment(session, plant, date(2023, 5, 1), 'Looking healthy!')

        # Get all plants
        plants = db_manager.get_all_plants(session)
        for plant in plants:
            print(plant)

        # Get measurements for a plant
        measurements = db_manager.get_measurements(session, plant)
        for measurement in measurements:
            print(measurement)

        # Get all nutrient types
        nutrient_types = db_manager.get_all_nutrient_types(session)
        for nutrient_type in nutrient_types:
            print(nutrient_type)

        # Get nutrients for a plant
        nutrients = db_manager.get_nutrients(session, plant)
        for nutrient in nutrients:
            print(nutrient)

        # Get comments for a plant
        comments = db_manager.get_comments(session, plant)
        for comment in comments:
            print(comment)