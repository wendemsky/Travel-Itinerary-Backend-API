# main.py

from fastapi import FastAPI, Depends, HTTPException, status, Query 
from sqlalchemy.orm import Session, joinedload, selectinload # For eager loading
from typing import List

# Import models, schemas, and db session getter
import models, schemas
from database import engine, get_db
from models import Base # Import Base for table creation
from sqlalchemy.exc import IntegrityError

# Create database tables if they don't exist (on app startup)
# In production, you'd likely use Alembic migrations
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Travel Itinerary API",
    description="API for creating and viewing travel itineraries for Phuket & Krabi.",
    version="0.1.0",
)

# === API Endpoints ===

# --- Itinerary Creation ---
@app.post(
    "/itineraries/",
    response_model=schemas.ItineraryDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new travel itinerary",
    tags=["Itineraries"]
)
def create_itinerary(
    itinerary: schemas.ItineraryCreate, db: Session = Depends(get_db)
):
    """
    Creates a new itinerary record along with its day structure.

    **(Validation)**:
    *   Ensures `duration_nights` > 0 (via Pydantic schema).
    *   Validates that all provided `accommodation_id`, `activity_ids`, `transfer_ids` exist in the database.
    *   Checks for duplicate `day_number` entries within the request.

    **(Error Handling)**:
    *   Returns `422 Unprocessable Entity` for schema validation errors (FastAPI default).
    *   Returns `400 Bad Request` for duplicate day numbers or missing related entity IDs.
    *   Returns `500 Internal Server Error` for unexpected database issues.

    **(Input Format Example)**:
    ```json
    {
      "name": "My Custom Phuket Trip",
      "duration_nights": 4,
      "region": "Phuket",
      "days": [
        {
          "day_number": 1,
          "day_summary": "Arrival and Beach",
          "accommodation_id": 1,
          "activity_ids": [],
          "transfer_ids": [1]
        },
        {
          "day_number": 2,
          "day_summary": "Island Tour",
          "accommodation_id": 1,
          "activity_ids": [1],
          "transfer_ids": []
        }
      ]
    }
    ```
    *(Note: Replace IDs with actual valid IDs from your database)*
    """
    # --- Input Validation ---
    # Check for duplicate day numbers in the input list
    if itinerary.days:
        day_numbers = [d.day_number for d in itinerary.days]
        if len(day_numbers) != len(set(day_numbers)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate day numbers found in the itinerary request."
            )

    # Collect all required foreign entity IDs from the request
    required_acc_ids = {d.accommodation_id for d in itinerary.days if d.accommodation_id}
    required_act_ids = {id for d in itinerary.days for id in d.activity_ids}
    required_trans_ids = {id for d in itinerary.days for id in d.transfer_ids}

    # --- Pre-fetch related entities to check existence ---
    try:
        # Fetch only the IDs for existence check, slightly more efficient
        existing_acc_ids = {res[0] for res in db.query(models.Accommodation.id).filter(models.Accommodation.id.in_(required_acc_ids)).all()}
        existing_act_ids = {res[0] for res in db.query(models.Activity.id).filter(models.Activity.id.in_(required_act_ids)).all()}
        existing_trans_ids = {res[0] for res in db.query(models.Transfer.id).filter(models.Transfer.id.in_(required_trans_ids)).all()}

        # Check for missing IDs
        missing_acc = required_acc_ids - existing_acc_ids
        missing_act = required_act_ids - existing_act_ids
        missing_trans = required_trans_ids - existing_trans_ids

        error_details = []
        if missing_acc: error_details.append(f"Accommodations not found with IDs: {missing_acc}")
        if missing_act: error_details.append(f"Activities not found with IDs: {missing_act}")
        if missing_trans: error_details.append(f"Transfers not found with IDs: {missing_trans}")

        if error_details:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, # Use 400 for bad client input data
                detail='; '.join(error_details)
            )

        # Retrieve full objects needed for relationships (can be optimized further if needed)
        existing_activities = {act.id: act for act in db.query(models.Activity).filter(models.Activity.id.in_(existing_act_ids)).all()}
        existing_transfers = {trans.id: trans for trans in db.query(models.Transfer).filter(models.Transfer.id.in_(existing_trans_ids)).all()}
        # Accommodation is linked via DayAccommodation, only ID needed during creation below

    except Exception as e:
         # Catch potential DB query errors during validation phase
         print(f"Error fetching related entities: {e}") # Log the error
         raise HTTPException(
             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
             detail="Failed to validate related itinerary items."
         )


    # --- Create Itinerary and Days ---
    db_itinerary = models.Itinerary(
        name=itinerary.name,
        duration_nights=itinerary.duration_nights,
        region=itinerary.region,
        is_recommended=False
    )
    db.add(db_itinerary)

    try:
        db.flush() # Get the itinerary ID before creating days

        if itinerary.days:
            for day_data in sorted(itinerary.days, key=lambda d: d.day_number): # Process in order
                db_day = models.Day(
                    itinerary_id=db_itinerary.id,
                    day_number=day_data.day_number,
                    day_summary=day_data.day_summary
                )
                db.add(db_day)
                db.flush() # Get day ID for linking

                # Link Accommodation
                if day_data.accommodation_id:
                    # Validation already done, directly create link
                    day_acc = models.DayAccommodation(
                        day_id=db_day.id,
                        accommodation_id=day_data.accommodation_id
                    )
                    db.add(day_acc)

                # Link Activities - NOTE: Simple append doesn't guarantee order if needed
                # For explicit order, need to manage the association table directly or use ordered list extension
                for act_id in day_data.activity_ids:
                    db_day.activities.append(existing_activities[act_id])

                # Link Transfers
                for trans_id in day_data.transfer_ids:
                    db_day.transfers.append(existing_transfers[trans_id])

        db.commit()
        db.refresh(db_itinerary) # Refresh to load relationships

    except IntegrityError as e:
        db.rollback()
        print(f"Database Integrity Error: {e}") # Log details
        # Example: FK constraint failed, Unique constraint failed etc.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, # Often caused by bad input (e.g., duplicate unique keys)
            detail=f"Database constraint violation. Check input data. Details: {e.orig}"
        )
    except Exception as e:
        db.rollback()
        print(f"Error during itinerary creation commit: {e}") # Log the error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while saving the itinerary."
        )

    # --- Eager Load for Response ---
    # Fetch again with eager loading for the response model
    try:
        db_itinerary_loaded = db.query(models.Itinerary).options(
            selectinload(models.Itinerary.days)
                .selectinload(models.Day.accommodation_link)
                .joinedload(models.DayAccommodation.accommodation),
            selectinload(models.Itinerary.days)
                .selectinload(models.Day.activities),
            selectinload(models.Itinerary.days)
                .selectinload(models.Day.transfers)
        ).filter(models.Itinerary.id == db_itinerary.id).one() # Use .one() as we expect it to exist
        return db_itinerary_loaded
    except Exception as e:
         print(f"Error fetching created itinerary for response: {e}") # Log the error
         raise HTTPException(
             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
             detail="Itinerary created, but failed to retrieve full details for response."
         )


# --- Itinerary Viewing (List) ---
@app.get(
    "/itineraries/",
    response_model=List[schemas.ItineraryList],
    summary="List all itineraries",
    tags=["Itineraries"]
)
def read_itineraries(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieves a list of all itineraries (both recommended and user-created).
    Supports pagination using `skip` and `limit` query parameters.

    **(Example Response - List)**:
    ```json
    [
      {
        "name": "Phuket Explorer (3 Nights)",
        "duration_nights": 3,
        "region": "Phuket",
        "id": 1,
        "is_recommended": true
      },
      {
        "name": "My Custom Phuket Weekend",
        "duration_nights": 2,
        "region": "Phuket",
        "id": 8,
        "is_recommended": false
      }
    ]
    ```
    """
    itineraries = db.query(models.Itinerary).offset(skip).limit(limit).all()
    return itineraries


# --- Itinerary Viewing (Detail) ---
@app.get(
    "/itineraries/{itinerary_id}",
    response_model=schemas.ItineraryDetail,
    summary="Get details of a specific itinerary",
    tags=["Itineraries"]
)
def read_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the full details for a specific itinerary by its ID,
    including day-by-day plans with accommodations, activities, and transfers.

    **(Example Response - Detail for ID 1)**:
    ```json
    {
      "name": "Phuket Explorer (3 Nights)",
      "duration_nights": 3,
      "region": "Phuket",
      "id": 1,
      "is_recommended": true,
      "created_at": "2023-10-27T10:00:00Z",
      "updated_at": null,
      "days": [
        {
          "id": 1,
          "day_number": 1,
          "day_summary": "Arrive in Phuket, transfer to Patong area.",
          "accommodation_link": {
            "accommodation": {
              "name": "Phuket Marriott Resort & Spa, Merlin Beach",
              "location": "Patong, Phuket",
              "type": "Resort",
              "rating": 5,
              "id": 1
            }
          },
          "activities": [],
          "transfers": [
            {
              "description": "Phuket Airport to Hotel Transfer",
              "from_location": "Phuket Airport (HKT)",
              "to_location": "Phuket Hotel",
              "method": "Private Car/Minivan",
              "duration_minutes": 60,
              "id": 1
            }
          ]
        },
        {
           "id": 2,
           "day_number": 2,
           // ... rest of day 2 details ...
        }
        // ... other days ...
      ]
    }
    ```
    *(Note: `created_at`/`updated_at` format/presence depends on DB timezone settings)*
    """
    itinerary = db.query(models.Itinerary).options(
         # ... eager loading ...
    ).filter(models.Itinerary.id == itinerary_id).first()

    if itinerary is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found")
    return itinerary



# --- MCP Server Endpoint (Requirement 3) ---
@app.get(
    "/itineraries/recommended/",
    response_model=List[schemas.ItineraryDetail],
    summary="Get recommended itineraries by duration (2-8 nights)", 
    tags=["Recommendations (MCP)"]
)
def get_recommended_itineraries_by_duration(
    duration: int = Query(
        ...,
        ge=2,  # <<< Add: Greater than or equal to 2
        le=8,  # <<< Add: Less than or equal to 8
        description="Number of nights for the desired itinerary (Must be between 2 and 8)" 
    ),
    db: Session = Depends(get_db)
):
    """
    **(MCP Server Logic)** - Retrieves recommended itineraries matching the
    specified number of nights, restricted to durations between 2 and 8 nights.

    Returns a list of itineraries marked as 'recommended' that have the exact
    `duration_nights` specified. Includes full day-by-day details.
    """
    recommended_itineraries = db.query(models.Itinerary).options(
        # Eager loading options... (keep as before)
        selectinload(models.Itinerary.days)
            .selectinload(models.Day.accommodation_link)
            .joinedload(models.DayAccommodation.accommodation),
        selectinload(models.Itinerary.days)
            .selectinload(models.Day.activities),
        selectinload(models.Itinerary.days)
            .selectinload(models.Day.transfers)
    ).filter(
        models.Itinerary.is_recommended == True,
        models.Itinerary.duration_nights == duration # duration is now guaranteed to be 2-8
    ).order_by(models.Itinerary.id).all()

    return recommended_itineraries

# Add a root endpoint for basic check
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Travel Itinerary API!"}

# If you need to run this directly using uvicorn:
if __name__ == "__main__":
   import uvicorn
   uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)