from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class TripRequest(BaseModel):
    location: str = Field(
        ..., description="The destination the user wants to visit (e.g., Rome, Italy)."
    )
    from_date: date = Field(..., description="The start date of the trip.")
    to_date: date = Field(..., description="The end date of the trip.")
    travellers: int = Field(..., description="Total number of people traveling.")
    home_country: str = Field(..., description="User's current country of residence.")
    preferences: List[str] = Field(
        ..., description="User's travel preferences like Food, Adventure, Culture, etc.")
    nearest_airport: str = Field(..., description="Nearest Airport from user's current location")
    dest_airport: Optional[str] = Field(None, description="Airport where user want to go")
    city: Optional[str] = Field(None, description="Based on location entered get the city IATA code")
    @property
    def duration_days(self) -> int:
        return (self.to_date - self.from_date).days

class FlightInfo(BaseModel):
    airline: str
    from_airport: str
    to_airport: str
    departure_time: str  
    arrival_time: str
    duration: str
    price: str  
    currency: Optional[str] = None  


class Transportation(BaseModel):
    departing_flights: List[FlightInfo]
    returning_flights: List[FlightInfo]


class HotelInfo(BaseModel):
    hotel_name : str
    check_in_date : date
    check_out_date : date
    duration: str
    per_day_price: str  = Field(description="Daily price of hotel booking")
    total_price: str = Field(description="Total price of hotel booking")
    currency: Optional[str] = None  
    guests: int


class BudgetInfo(BaseModel):
    activities_cost: str
    transportation_cost: str
    hotel_cost: str
    miscellaneous_cost: str
    food_estimate: str
    internal_travel_cost: str
    total_cost: str
    per_person_cost: str


class TripItinerary(BaseModel):
    user_input: TripRequest
    llm_plan: str | None = None
    activities: Optional[str] = None
    itinerary: dict[str, List[str]] | None = None
    hotels: List[HotelInfo] | None = None
    budget_estimate: BudgetInfo | None = None
    currency: str | None = None
    notes: str | None = None
    transportation: Optional[Transportation] = None
    weather: str | None = None

