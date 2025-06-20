from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from core.state import TripRequest, TripItinerary
from core.utils import llm_model, get_prompt


def activities_node(state: TripItinerary):
    template = get_prompt("llm_daily_plan")
    input_variables = {
        "location": state.user_input.location,
        "from_date": state.user_input.from_date,
        "to_date": state.user_input.to_date,
        "travellers": state.user_input.travellers,
        "home_country": state.user_input.home_country,
        "preferences": ", ".join(state.user_input.preferences),
        "duration_days": state.user_input.duration_days,

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
        ],
    )

    chain = prompt | llm_model

    response = chain.invoke(input_variables)

    return TripItinerary(
    user_input=state.user_input,
    llm_plan=state.llm_plan,
    activities=response.content
)
