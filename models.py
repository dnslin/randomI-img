from sqlalchemy import Column, Integer, Text
from database import Base

class ImageUrl(Base):
    __tablename__ = "image_urls"

    id = Column(Integer, primary_key=True, index=True)
    page = Column(Integer)
    url = Column(Text) 