# Travel Itinerary Backend API

## Description

This project is a backend system for managing travel itineraries, built as part of the Full-stack SDE Intern Assignment for Often. It provides a RESTful API for creating and viewing travel itineraries, focusing on the Phuket and Krabi regions of Thailand. It also includes a mechanism to retrieve pre-defined recommended itineraries based on the duration (number of nights).

## Features

*   **Database:** Uses SQLAlchemy to model itineraries, days, accommodations, activities, and transfers, with relationships between them. Includes a seeding script for sample data. Uses SQLite for simplicity.
*   **RESTful API:** Built with FastAPI, providing endpoints for:
    *   Creating new custom itineraries.
    *   Listing all itineraries.
    *   Viewing the detailed plan of a specific itinerary.
*   **Recommended Itineraries (MCP):** An endpoint to fetch recommended itineraries filtered by duration (specifically for 2 to 8 nights).
*   **Validation:** Uses Pydantic for request/response validation and FastAPI's features for parameter validation.
*   **API Documentation:** Auto-generated interactive API documentation available via Swagger UI and ReDoc.

## Technology Stack

*   **Language:** Python 3.10+
*   **Framework:** FastAPI
*   **Database ORM:** SQLAlchemy
*   **Data Validation:** Pydantic
*   **Database:** SQLite (default)
*   **API Server:** Uvicorn

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Make sure you have a `requirements.txt` file (generate using `pip freeze > requirements.txt` in your activated environment).
    ```bash
    pip install -r requirements.txt
    ```

## Database Setup

The application uses SQLite, and the database file (`travel_itinerary.db`) will be created in the project's root directory.

*   **Seed the Database:** Run the seeding script to create the necessary tables (if they don't exist) and populate the database with sample accommodations, activities, transfers, and recommended itineraries (2-8 nights) for Phuket and Krabi.
    ```bash
    python seed.py
    ```
    *(Note: The seed script currently drops and recreates tables each time it's run. Modify if persistence across runs is needed without reseeding recommended data.)*

## Running the Application

*   **Start the FastAPI Server:** Use Uvicorn to run the application. The `--reload` flag enables auto-reloading during development.
    ```bash
    uvicorn main:app --reload --port 8000
    ```
    The API will be available at `http://localhost:8000`.

## API Usage

Once the server is running, you can interact with the API:

*   **Interactive Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
*   **Alternative Docs (ReDoc):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

These interfaces allow you to explore and test the API endpoints directly from your browser.

**Key Endpoints:**

*   `POST /itineraries/`: Create a new custom itinerary.
*   `GET /itineraries/`: List all itineraries.
*   `GET /itineraries/{itinerary_id}`: Get details of a specific itinerary.
*   `GET /itineraries/recommended/?duration={nights}`: Get recommended itineraries for a duration between 2 and 8 nights.
