from sqlalchemy import create_engine, Column, String, Integer, Numeric, Date
from sqlalchemy.orm import sessionmaker, declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PhoneDB(Base):
    __tablename__ = 'phone_petrov'

    id = Column(Integer, primary_key=True)
    model = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    release_date = Column(Date)
    description = Column(String, nullable=True)
