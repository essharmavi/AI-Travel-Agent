# 🧳 AI Travel Planner

An intelligent travel planning assistant powered by LangChain, OpenAI, and Amadeus APIs. Just tell the app where and when you're going, and it will plan your entire trip – flights, hotels, activities, weather forecast, and estimated budget – all personalized to your preferences.

## ✨ Features

- 🌍 Destination-aware itinerary generation
- 🛫 Flight search (departure & return)
- 🏨 Hotel availability with price breakdown
- ☀️ Weather forecast for the destination
- 🏖️ Daily activity planning based on preferences
- 💰 Budget estimation with per-person cost
- 📊 Streamlit frontend for interactive user input
- 🧠 Powered by LLMs (OpenAI + LangChain)
- 🔗 Integrated with Amadeus Travel APIs

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/ai-travel-planner.git](https://github.com/essharmavi/AI-Travel-Agent.git)
cd ai-travel-planner
```

### 2. Set up the virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Set up API Keys
Create a .env file in the project root with the following:

OPENAI_API_KEY=your_openai_api_key
AMADEUS_API_KEY=your_amadeus_api_key
AMADEUS_API_SECRET=your_amadeus_api_secret

### 4. Run the app
```bash
streamlit run app.py
```
## Project Structure
.
├── app.py                     # Streamlit UI
├── core/
│   ├── state.py               # Pydantic models for trip data
│   ├── utils.py               # LLM, prompts, helper functions
│   ├── prompts.json           # Prompt templates
│   └── airport_data.py        # Static data for airport codes
├── nodes/
│   ├── flight_node.py
│   ├── hotel_node.py
│   ├── activity_node.py
│   ├── weather_node.py
│   └── budget_node.py
├── workflows/
│   └── travel_graph.py        # LangGraph to orchestrate the trip pipeline
├── requirements.txt
└── README.md

 ## Tech Stack
	•	LangChain + LangGraph: LLM orchestration & agent workflows
	•	OpenAI GPT: Generative AI for itinerary, budget, etc.
	•	Amadeus API: Real-time flight and hotel data
	•	Streamlit: Frontend UI
	•	OpenWeatherMap API: Get real- time weather data
  •	Pydantic: State management with validation

### Example Use Case

“Plan a 7-day cultural and food-focused trip to Rome, Italy from India starting July 1st.”

You’ll get:
	•	✈️ Top 3 flights (departure & return)
	•	🏨 Top 3 hotel options with pricing
	•	☀️ Weather forecast for the whole stay
	•	🗺️ Day-by-day itinerary with local attractions and food spots
	•	💰 Cost breakdown with per-person estimate

⸻

### API Notes
	•	You’ll need valid credentials for:
	•	OpenAI API
	•	Amadeus for Developers
 
---

