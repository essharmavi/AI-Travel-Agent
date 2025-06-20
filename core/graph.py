from langgraph.graph import START, END, StateGraph
from core.state import TripItinerary
from nodes.activity_node import activities_node
from nodes.budget_node import budget_node
from nodes.hotel_node import hotel_node
from nodes.llm_node import llm_node
from nodes.transportation_node import transportation_node
from nodes.weather_node import weather_node

def build_travel_graph():
    builder = StateGraph(TripItinerary)

    builder.add_node("llm_plan", llm_node)
    builder.add_node("transportation", transportation_node)
    builder.add_node("hotel", hotel_node)
    builder.add_node("activity", activities_node)
    builder.add_node("weather", weather_node)
    builder.add_node("budget", budget_node)

    builder.set_entry_point("llm_plan")
    builder.add_edge("llm_plan", "activity")
    builder.add_edge("activity", "transportation")
    builder.add_edge("transportation", "hotel")
    builder.add_edge("hotel", "weather")
    builder.add_edge("weather", "budget")

    builder.set_finish_point("budget")

    return builder.compile()

