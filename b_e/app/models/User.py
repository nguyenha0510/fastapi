from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, BigInteger
from sqlalchemy.orm import relationship
from b_e.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    name = Column(String(100), nullable=False)
    account = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)  # lưu hash, không lưu plain text!

    is_block = Column(Boolean, default=False, nullable=False)
    count_error_authentication = Column(Integer, default=0, nullable=False)
    block_to_date = Column(DateTime, nullable=True)

    # Ref to Group (many-to-one)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    group = relationship("Group", back_populates="users", lazy="selectin")

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())