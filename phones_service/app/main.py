import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from database import database_phones as database
from database.database_phones import PhoneDB
from model.model_phones import Phone

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
async def add_phone(phone: Phone, db: db_dependency):
    new_phone = PhoneDB(**phone.dict())
    db.add(new_phone)
    db.commit()
    db.refresh(new_phone)
    return new_phone


@app.get("/get_phones")
async def get_phones(db: db_dependency):
    return db.query(PhoneDB).all()


@app.get("/get_phone_by_id")
async def get_phone_by_id(phone_id: int, db: db_dependency):
    phone = db.query(PhoneDB).filter(PhoneDB.id == phone_id).first()
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found")
    return phone


@app.put("/update_phone")
async def update_phone(phone_id: int, phone: Phone, db: db_dependency):
    db_phone = db.query(PhoneDB).filter(PhoneDB.id == phone_id).first()
    if not db_phone:
        raise HTTPException(status_code=404, detail="Phone not found")
    for var, value in phone.dict(exclude_unset=True).items():
        setattr(db_phone, var, value)
    db.commit()
    return db_phone


@app.delete("/delete_phone")
async def delete_phone(phone_id: int, db: db_dependency):
    db_phone = db.query(PhoneDB).filter(PhoneDB.id == phone_id).first()
    if not db_phone:
        raise HTTPException(status_code=404, detail="Phone not found")
    db.delete(db_phone)
    db.commit()
    return {"message": "Phone deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
