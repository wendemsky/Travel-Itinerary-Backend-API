# models.py

import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Date, ForeignKey,
    Table, MetaData, DateTime, Text, UniqueConstraint 
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()
metadata = MetaData()

# Association table for Day <-> Activity (Many-to-Many)
day_activity_association = Table(
    'day_activity_association', Base.metadata,
    Column('day_id', Integer, ForeignKey('days.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True),
    Column('order', Integer, default=0) # To order activities within a day
)

# Association table for Day <-> Transfer (Many-to-Many)
day_transfer_association = Table(
    'day_transfer_association', Base.metadata,
    Column('day_id', Integer, ForeignKey('days.id'), primary_key=True),
    Column('transfer_id', Integer, ForeignKey('transfers.id'), primary_key=True),
    Column('order', Integer, default=0) # To order transfers within a day
)

class Itinerary(Base):
    __tablename__ = 'itineraries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    duration_nights = Column(Integer, nullable=False)
    region = Column(String, index=True)
    is_recommended = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    days = relationship("Day", back_populates="itinerary", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Itinerary(id={self.id}, name='{self.name}', duration={self.duration_nights} nights)>"

class Day(Base):
    __tablename__ = 'days'
    # __table_args__ = (
    #     UniqueConstraint('itinerary_id', 'day_number', name='_itinerary_day_uc'),

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey('itineraries.id'), nullable=False)
    day_number = Column(Integer, nullable=False)
    day_summary = Column(Text, nullable=True)

    itinerary = relationship("Itinerary", back_populates="days")

    activities = relationship(
        "Activity",
        secondary=day_activity_association,
        back_populates="days",
        order_by="day_activity_association.c.order"
    )
    transfers = relationship(
        "Transfer",
        secondary=day_transfer_association,
        back_populates="days",
        order_by="day_transfer_association.c.order"
    )
    accommodation_link = relationship("DayAccommodation", uselist=False, back_populates="day", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Day(id={self.id}, itinerary_id={self.itinerary_id}, day_number={self.day_number})>"

class Accommodation(Base):
    __tablename__ = 'accommodations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    location = Column(String, index=True)
    type = Column(String, nullable=True) # e.g., Hotel, Villa, Resort
    rating = Column(Integer, nullable=True) # e.g., 3, 4, 5 stars

    # Relationship back to the days it's assigned to (via DayAccommodation)
    day_assignments = relationship("DayAccommodation", back_populates="accommodation")

    def __repr__(self):
        return f"<Accommodation(id={self.id}, name='{self.name}')>"

# Link table to associate a specific Accommodation with a specific Day (for the night)
class DayAccommodation(Base):
    __tablename__ = 'day_accommodations'

    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey('days.id'), unique=True, nullable=False) # Each day link is unique
    accommodation_id = Column(Integer, ForeignKey('accommodations.id'), nullable=False)

    day = relationship("Day", back_populates="accommodation_link")
    accommodation = relationship("Accommodation", back_populates="day_assignments")

    def __repr__(self):
        return f"<DayAccommodation(day_id={self.day_id}, accommodation_id={self.accommodation_id})>"


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    location = Column(String, index=True)
    duration_hours = Column(Integer, nullable=True) # Approximate duration
    type = Column(String, nullable=True) # e.g., Tour, Sightseeing, Beach, Adventure

    # Relationship back to the days it's part of
    days = relationship(
        "Day",
        secondary=day_activity_association,
        back_populates="activities"
    )

    def __repr__(self):
        return f"<Activity(id={self.id}, name='{self.name}')>"

class Transfer(Base):
    __tablename__ = 'transfers'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False) # e.g., Airport Pickup, Ferry to Krabi
    from_location = Column(String)
    to_location = Column(String)
    method = Column(String) # e.g., Private Car, Ferry, Speedboat
    duration_minutes = Column(Integer, nullable=True) # Approximate duration

    # Relationship back to the days it's part of
    days = relationship(
        "Day",
        secondary=day_transfer_association,
        back_populates="transfers"
    )

    def __repr__(self):
        return f"<Transfer(id={self.id}, description='{self.description}')>"

# Example setup for database connection (using SQLite for simplicity)
DATABASE_URL = "sqlite:///./travel_itinerary.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
