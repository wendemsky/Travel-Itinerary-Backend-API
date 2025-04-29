# schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

# --- Base Schemas (for shared fields) ---

class AccommodationBase(BaseModel):
    name: str
    location: Optional[str] = None
    type: Optional[str] = None
    rating: Optional[int] = None

class ActivityBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    duration_hours: Optional[int] = None
    type: Optional[str] = None

class TransferBase(BaseModel):
    description: str
    from_location: Optional[str] = None
    to_location: Optional[str] = None
    method: Optional[str] = None
    duration_minutes: Optional[int] = None

# --- Schemas for Reading Data (Responses) ---

class Accommodation(AccommodationBase):
    id: int

    class Config:
        orm_mode = True # Renamed from from_attributes=True in Pydantic v2

class Activity(ActivityBase):
    id: int

    class Config:
        orm_mode = True

class Transfer(TransferBase):
    id: int

    class Config:
        orm_mode = True

# Represents the accommodation linked to a day
class DayAccommodationDetail(BaseModel):
    accommodation: Accommodation

    class Config:
        orm_mode = True

# Structure for activities/transfers within a day in the response
class DayActivityDetail(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    duration_hours: Optional[int] = None
    type: Optional[str] = None
    order: Optional[int] = None # Include order if needed in response

    class Config:
        orm_mode = True

class DayTransferDetail(BaseModel):
    id: int
    description: str
    from_location: Optional[str] = None
    to_location: Optional[str] = None
    method: Optional[str] = None
    duration_minutes: Optional[int] = None
    order: Optional[int] = None # Include order if needed in response

    class Config:
        orm_mode = True


class DayDetail(BaseModel):
    id: int
    day_number: int
    day_summary: Optional[str] = None
    # Use the detailed schemas for nested data
    accommodation_link: Optional[DayAccommodationDetail] = None
    activities: List[Activity] = [] 
    transfers: List[Transfer] = []  

    class Config:
        orm_mode = True


class ItineraryBase(BaseModel):
    name: str
    duration_nights: int = Field(..., gt=0) # Ensure duration is positive
    region: Optional[str] = None

class ItineraryDetail(ItineraryBase):
    id: int
    is_recommended: bool
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    days: List[DayDetail] = [] # Include full day details

    class Config:
        orm_mode = True

class ItineraryList(ItineraryBase):
    id: int
    is_recommended: bool

    class Config:
        orm_mode = True


# --- Schemas for Creating Data (Requests) ---

# Define IDs for associating existing entities when creating
class ItemId(BaseModel):
    id: int

class DayCreateDetail(BaseModel):
    day_number: int
    day_summary: Optional[str] = None
    accommodation_id: Optional[int] = None # ID of accommodation for this day's night
    activity_ids: List[int] = [] # List of activity IDs for the day
    transfer_ids: List[int] = [] # List of transfer IDs for the day


class ItineraryCreate(ItineraryBase):

    days: List[DayCreateDetail] = []
