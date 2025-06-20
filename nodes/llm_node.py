from langchain_core.prompts import PromptTemplate
from core.state import TripRequest, TripItinerary
from core.utils import llm_model, get_prompt


def llm_node(state: TripRequest):
    template = get_prompt("llm_trip_plan")
    input_variables = {
        "location": state.location,
        "from_date": state.from_date,
        "to_date": state.to_date,
        "travellers": state.travellers,
        "home_country": state.home_country,
        "preferences": state.preferences,
        "duration_days": state.duration_days,
        "nearest_airport": state.nearest_airport
    }

    prompt = PromptTemplate(
        template=template,
        input_variables=[
            "location",
            "from_date", 
            "to_date",
            "travellers",
            "home_country",
            "preferences",
            "duration_days",
            "nearest_airport"
        ],
    )

    chain = prompt | llm_model

    response = chain.invoke(input_variables)

    airport_query = f"Nearest airport to travel location: {state.location}. Return one word airport code and nothing else."
    state.dest_airport = llm_model.invoke(airport_query).content.strip()

    city_query = f"Based on the location: {state.location} . Return the city's IATA code and nothing else."
    state.city = llm_model.invoke(city_query).content.strip()
    print(state.city)

    return TripItinerary(user_input=state, llm_plan=response.content)
