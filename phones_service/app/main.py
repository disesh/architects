import os
import uvicorn
from fastapi import FastAPI, status, Form, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from keycloak import KeycloakOpenID

from database import database_phones as database
from database.database_phones import PhoneDB
from model.model_phones import Phone

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def chech_for_role_test(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (chech_for_role_test(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.post("/add_phone")
async def add_phone(phone: Phone, db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        new_phone = PhoneDB(**phone.dict())
        db.add(new_phone)
        db.commit()
        db.refresh(new_phone)
        return new_phone
    else:
        return "Wrong JWT Token"


@app.get("/get_phones")
async def get_phones(db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        return db.query(PhoneDB).all()
    else:
        return "Wrong JWT Token"


@app.get("/get_phone_by_id")
async def get_phone_by_id(phone_id: int, db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        phone = db.query(PhoneDB).filter(PhoneDB.id == phone_id).first()
        if not phone:
            raise HTTPException(status_code=404, detail="Phone not found")
        return phone
    else:
        return "Wrong JWT Token"


@app.put("/update_phone")
async def update_phone(phone_id: int, phone: Phone, db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        db_phone = db.query(PhoneDB).filter(PhoneDB.id == phone_id).first()
        if not db_phone:
            raise HTTPException(status_code=404, detail="Phone not found")
        for var, value in phone.dict(exclude_unset=True).items():
            setattr(db_phone, var, value)
        db.commit()
        return db_phone
    else:
        return "Wrong JWT Token"


@app.delete("/delete_phone")
async def delete_phone(phone_id: int, db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        db_phone = db.query(PhoneDB).filter(PhoneDB.id == phone_id).first()
        if not db_phone:
            raise HTTPException(status_code=404, detail="Phone not found")
        db.delete(db_phone)
        db.commit()
        return {"message": "Phone deleted"}
    else:
        return "Wrong JWT Token"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
