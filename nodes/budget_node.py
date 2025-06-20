from core.state import TripItinerary, BudgetInfo
from langchain.prompts import PromptTemplate
from core.utils import llm_model, get_prompt

def budget_node(state: TripItinerary):
    user_input = state.user_input
    activities = state.activities
    transportation = state.transportation
    home_country = state.user_input.home_country
    hotel = state.hotels
    template = get_prompt("")
    prompt = PromptTemplate(template = template, input_variables=["activities", "transportation","hotel", "user_input", "home_country"])
    chain = prompt | llm_model
    response = chain.invoke({
        "activities": activities, 
        "transportation": transportation,
        "hotel": hotel, 
        "user_input": user_input
        "home_country": home_country
    })
    state.budget_estimate = response.content
    return TripItinerary(
        user_input=state.user_input,
        llm_plan=state.llm_plan,
        activities=state.activities,
        itinerary=state.itinerary,
        hotels=state.hotels,
        budget_estimate=state.budget_estimate,
        currency=state.currency,
        transportation=state.transportation,
        weather=state.weather
    )
