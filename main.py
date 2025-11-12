import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import db, create_document, get_documents

app = FastAPI(title="WeebTours API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FAQItem(BaseModel):
    question: str
    answer: str


@app.get("/")
def read_root():
    return {"message": "WeebTours Backend Running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from WeebTours API"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# ===== WeebTours Domain Models (request bodies) =====
class TourIn(BaseModel):
    name: str
    destination: str
    start_date: str
    duration_days: int
    price: float
    summary: str
    highlights: Optional[List[str]] = None
    cover_image: Optional[str] = None


class BookingIn(BaseModel):
    tour_id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    travelers: int = 1
    notes: Optional[str] = None


@app.get("/api/tours")
def list_tours(limit: int = 20):
    try:
        items = get_documents("tour", {}, limit)
        # Convert ObjectId to string
        for item in items:
            item["id"] = str(item.pop("_id"))
        return {"tours": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/tours")
def create_tour(tour: TourIn):
    try:
        # Convert start_date to ISO date if needed
        try:
            datetime.fromisoformat(tour.start_date)
        except Exception:
            raise HTTPException(status_code=400, detail="start_date must be ISO format YYYY-MM-DD")
        tour_dict = tour.model_dump()
        tour_id = create_document("tour", tour_dict)
        return {"id": tour_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/bookings")
def create_booking(booking: BookingIn):
    try:
        booking_dict = booking.model_dump()
        booking_id = create_document("booking", booking_dict)
        return {"id": booking_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/faqs")
def get_faqs():
    faqs: List[FAQItem] = [
        {"question": "How do I book a tour?", "answer": "Choose a tour, hit Book Now, and fill out your details."},
        {"question": "What payment methods are accepted?", "answer": "We accept major cards and secure online transfers."},
        {"question": "What is the cancellation policy?", "answer": "Free cancellation up to 7 days before departure."},
        {"question": "Is travel insurance included?", "answer": "Insurance is optional and can be added at checkout."},
        {"question": "How can I contact support?", "answer": "Email support@weebtours.com or call +1 (555) 123-4567."}
    ]
    return {"faqs": faqs}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
