import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from database import database as database
from database.database import PhoneInventoryDB
from model.model import PhoneInventory

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'Service alive'}


@app.post("/add_phone")
async def add_phone(phone: PhoneInventory, db: db_dependency):
    db_phone = PhoneInventoryDB(**phone.dict())
    db.add(db_phone)
    db.commit()
    return db_phone


@app.get("/phones")
async def list_phones(db: db_dependency):
    phones = db.query(PhoneInventoryDB).all()
    return phones


@app.post("/sell_phone")
async def sell_phone(id: int, db: db_dependency):
    phone = db.query(PhoneInventoryDB).filter(PhoneInventoryDB.id == id).first()
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found")
    if phone.quantity < 1:
        raise HTTPException(status_code=400, detail="No phone available to sell")
    phone.quantity -= 1
    db.commit()
    return phone


@app.post("/increase_phone_stock")
async def increase_phone_stock(id: int, amount: int, db: db_dependency):
    phone = db.query(PhoneInventoryDB).filter(PhoneInventoryDB.id == id).first()
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found")
    phone.quantity += amount
    db.commit()
    return phone


@app.delete("/delete_phone")
async def delete_phone(id: int, db: db_dependency):
    phone = db.query(PhoneInventoryDB).filter(PhoneInventoryDB.id == id).first()
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found")
    db.delete(phone)
    db.commit()
    return {"message": "Phone deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
