from core.utils import llm_model, weather, get_prompt
from core.state import TripRequest, TripItinerary
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
def weather_node(state: TripItinerary) -> TripItinerary:
    
    tools = [
        Tool(
            name="WeatherTool",
            func=weather.run,
            description="Get weather information and forecasts for a specific location and date range"
        )
    ]

    template = get_prompt("parse_weather_updates")
    
    prompt = PromptTemplate(
        template=template,
        input_variables=['location', 'from_date', 'to_date', 'tools', 'tool_names', 'input', 'agent_scratchpad']
    )
    
    agent = create_react_agent(llm_model, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3
    )
    
    input_text = f"Get weather information for {state.user_input.location} from {state.user_input.from_date} to {state.user_input.to_date}"
    
    try:
        response = agent_executor.invoke({
            "input": input_text,
            "location": state.user_input.location,
            "from_date": state.user_input.from_date,
            "to_date": state.user_input.to_date
        })
        weather_data = response.get('output', 'Weather information not available')
    except Exception as e:
        weather_data = f"Weather unavailable: {e}"
    
    return TripItinerary(
        user_input=state.user_input,
        llm_plan=state.llm_plan,
        activities=state.activities,
        itinerary=state.itinerary,
        hotels=state.hotels,
        budget_estimate=state.budget_estimate,
        currency=state.currency,
        transportation=state.transportation,
        weather=weather_data
    )