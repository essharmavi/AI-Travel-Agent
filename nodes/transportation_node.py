from core.utils import llm_model, get_prompt, amadeus
from core.state import TripRequest, TripItinerary, Transportation, FlightInfo
from langchain_core.prompts import PromptTemplate
from amadeus import ResponseError
import json
import time


def transportation_node(state: TripItinerary) -> TripItinerary:
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=state.user_input.nearest_airport,
            destinationLocationCode=state.user_input.dest_airport,
            departureDate=str(state.user_input.from_date),
            returnDate=str(state.user_input.to_date),
            adults=state.user_input.travellers
        )
    except ResponseError as error:
        raise error

    flight_data_json = response.data
    departing_flights_list = [flight['itineraries'][0]['segments'][0] for flight in flight_data_json]
    returning_flights_list = [flight['itineraries'][0]['segments'][-1] for flight in flight_data_json]


    common_input = {
        "home_country": state.user_input.home_country,
        "destination_country": state.user_input.location,
    }

    # Departing prompt
    dep_template = get_prompt("parse_departing_flights")
    dep_prompt = PromptTemplate(template=dep_template, input_variables=["home_country", "destination_country", "departing_flight_data"])
    dep_chain = dep_prompt | llm_model
    dep_result = dep_chain.invoke({**common_input, "departing_flight_data": departing_flights_list})
    print("Got Departing Flights")
    time.sleep(90)
    # Returning prompt
    ret_template = get_prompt("parse_returning_flights")
    ret_prompt = PromptTemplate(template=ret_template, input_variables=["home_country", "destination_country", "returning_flight_data"])
    ret_chain = ret_prompt | llm_model
    ret_result = ret_chain.invoke({**common_input, "returning_flight_data": returning_flights_list})
    print("Got Retruning Flights")
    time.sleep(90)
    print(dep_result.content)
    print(ret_result.content)
    transport_data = {
    **json.loads(dep_result.content),
    **json.loads(ret_result.content)
}

    transportation = Transportation(
        departing_flights=[FlightInfo(**f) for f in transport_data["departing_flights"]],
        returning_flights=[FlightInfo(**f) for f in transport_data["returning_flights"]],
    )


    return TripItinerary(
        user_input=state.user_input,
        llm_plan=state.llm_plan,
        activities=state.activities,
        itinerary=state.itinerary,
        hotels=state.hotels,
        budget_estimate=state.budget_estimate,
        currency=state.currency,
        notes=state.notes,
        transportation=transportation
    )
