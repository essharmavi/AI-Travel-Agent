import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from amadeus import Client
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
AMADEUS_API_KEY = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_API_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm_model = ChatOpenAI(model="gpt-4.1", api_key=OPEN_API_KEY, temperature=0.0)

amadeus = Client(
    client_id=AMADEUS_API_KEY,
    client_secret=AMADEUS_API_SECRET
)

weather = OpenWeatherMapAPIWrapper()

PROMPT_FILE = Path(__file__).parent / "prompt.json"

def get_prompt(name: str) -> str:
    with open(PROMPT_FILE, "r") as file:
        return json.load(file)[name]
