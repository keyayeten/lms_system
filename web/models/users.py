from sqlalchemy import Column, Integer, String
from core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)

    def __repr__(self):
        return "<User(id={id}, username={username}, hashed_password={hashed_password})>".format(
            id=self.id,
            username=self.name,
            hashed_password=self.hashed_password,
        )
