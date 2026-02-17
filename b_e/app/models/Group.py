from sqlalchemy import Column, Integer, String, BigInteger
from b_e.database import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    name = Column(String(100), unique=True, nullable=False, index=True)