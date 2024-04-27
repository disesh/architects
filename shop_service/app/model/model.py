from pydantic import BaseModel
from typing import Optional

class PhoneInventory(BaseModel):
    id: Optional[int]
    name: str
    quantity: int
