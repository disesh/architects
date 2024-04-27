from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Phone(BaseModel):
    id: Optional[int] = Field(None, example=1)
    model: str = Field(..., example="Galaxy S21")
    brand: str = Field(..., example="Samsung")
    price: float = Field(..., example=799.99)
    release_date: Optional[date] = Field(None, example="2021-01-29")
    description: Optional[str] = Field(None, example="Latest model with 5G connectivity.")
