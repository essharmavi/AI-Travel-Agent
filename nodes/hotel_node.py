from core.utils import llm_model, get_prompt, amadeus
from core.state import TripRequest, TripItinerary, HotelInfo
from langchain_core.prompts import PromptTemplate
from amadeus import ResponseError
import json
from datetime import datetime

def extract_hotel_data(hotel_offer_response):
    hotel_list = []

    for hotel_entry in hotel_offer_response:
        hotel_name = hotel_entry["hotel"]["name"]
        available = hotel_entry["available"]
        offer = hotel_entry["offers"][0]
        price_info = offer["price"]
        guests = offer["guests"]["adults"]
        
        check_in = datetime.strptime(offer["checkInDate"], "%Y-%m-%d")
        check_out = datetime.strptime(offer["checkOutDate"], "%Y-%m-%d")
        num_nights = (check_out - check_in).days
        total_price = float(price_info["total"])
        per_night_price = round(total_price / num_nights, 2)

        if available:
            hotel_list.append({
                "hotel_name": hotel_name,
                "check_in_date": offer["checkInDate"],
                "check_out_date": offer["checkOutDate"],
                "duration": f"{offer['checkInDate']} to {offer['checkOutDate']}",
                "guests": guests,
                "total_price": price_info["total"],
                "per_day_price": str(per_night_price),
                "currency": price_info["currency"]
            })

    return hotel_list



def hotel_node(state: TripItinerary) -> TripItinerary:


    city_code = str(state.user_input.city)
    print(city_code)
    hotels_by_city = amadeus.reference_data.locations.hotels.by_city.get(
            cityCode=city_code
        )
    hotel_ids = [hotel.get('hotelId') for hotel in hotels_by_city.data]
    print(hotel_ids[:10])

    check_in_date = state.transportation.departing_flights[0].arrival_time.split('T')[0]
    check_out_date = str(state.user_input.to_date)

    hotels_list = []
    valid_hotel_ids = []
    for id in hotel_ids[:100]:
        try:
            offers = amadeus.shopping.hotel_offers_search.get(
            hotelIds=str(id),
            adults=state.user_input.travellers,
            checkInDate=check_in_date,
            checkOutDate=check_out_date)

            hotels_list.extend(extract_hotel_data(offers.data))
            valid_hotel_ids.append(id)

        except ResponseError as error:
                continue

    top_hotels_list_3 = sorted(hotels_list, key=lambda i: float(i["total_price"]))[:5]
    state.hotels = top_hotels_list_3

    return TripItinerary(
        user_input=state.user_input,
        llm_plan=state.llm_plan,
        activities=state.activities,
        itinerary=state.itinerary,
        hotels=state.hotels,
        budget_estimate=state.budget_estimate,
        currency=state.currency,
        notes=state.notes,
        transportation=state.transportation
    )
