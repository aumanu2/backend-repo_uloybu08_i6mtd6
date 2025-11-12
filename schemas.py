"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# WeebTours specific schemas

class Tour(BaseModel):
    """
    Tours offered by WeebTours
    Collection name: "tour"
    """
    name: str
    destination: str
    start_date: date
    duration_days: int = Field(..., gt=0)
    price: float = Field(..., ge=0)
    summary: str
    highlights: List[str] = []
    cover_image: Optional[str] = None

class Booking(BaseModel):
    """
    Tour bookings
    Collection name: "booking"
    """
    tour_id: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    travelers: int = Field(1, gt=0)
    notes: Optional[str] = None

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
