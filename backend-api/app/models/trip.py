from sqlalchemy import Column, String, Numeric, JSON
from app.database.base import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(String, primary_key=True)
    destination = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    budget_inr = Column(Numeric)
    user_inputs = Column(JSON)
    generated_itinerary = Column(JSON)