import streamlit as st
import pycountry
from core.state import TripRequest
from core.airport_data import city_to_airport
from core.graph import build_travel_graph

country_list = sorted([country.name for country in pycountry.countries])

st.title("AI Travel Agent")
st.markdown("Tell us about your trip, and let AI plan it for you.")

with st.form("trip_form"):
    # Location Input
    location = st.text_input(
        label="Where do you want to go (city, country)?", max_chars=50, placeholder="Rome, Italy"
    )

    # Date Inputs
    from_date = st.date_input(
        label="Start Date", min_value="today", format="MM/DD/YYYY"
    )

    to_date = st.date_input(label="End Date", min_value=from_date, format="MM/DD/YYYY")

    # Number of Travellers
    travellers = st.number_input(
        label="Number of Travelers", min_value=1, max_value=20, step=1, value=1
    )

    # Current Country
    home_country = st.selectbox("Where are you currently based?", country_list)

    #Nearest Airport
    nearest_airport = st.selectbox("What is your nearest airport?", city_to_airport)

    # Trip Type
    trip_type = st.selectbox(
        "What's the purpose of your trip?",
        [
            "Vacation",
            "Business",
            "Honeymoon",
            "Solo Adventure",
            "Family",
            "Backpacking",
        ],
    )

    # Preferences
    preferences = st.multiselect(
        label="Travel Preferences",
        options=["Cultural", "Adventure", "Relaxation", "Nightlife", "Nature", "Food"],
        default=["Cultural", "Food"],
    )

    submitted = st.form_submit_button("Plan My Trip")

if submitted:
    if not location:
        st.warning("Please enter a destination.")
    elif to_date < from_date:
        st.warning("End date must be after start date.")
    else:
        with st.spinner("Generating your itinerary..."):
            trip_request = TripRequest(
                location=location,
                from_date=from_date,
                to_date=to_date,
                travellers=travellers,
                home_country=home_country,
                preferences=preferences,
                nearest_airport=nearest_airport.split("(")[0].strip()
            )

            itinerary = build_travel_graph(trip_request)

        st.success(f"Planned a {trip_request.duration_days}-day trip to {location} for {travellers} traveler(s) from {home_country}.")
        st.info(f"Preferences selected: {', '.join(preferences)}")

        st.header("🛫 Flights")
        if itinerary.transportation:
            with st.expander("Departing Flights"):
                for flight in itinerary.transportation.departing_flights:
                    st.markdown(f"**{flight.airline}**: {flight.from_airport} ➡️ {flight.to_airport}")
                    st.write(f"Departure: {flight.departure_time} | Arrival: {flight.arrival_time}")
                    st.write(f"Duration: {flight.duration} | Price: {flight.price} {flight.currency or ''}")
                    st.markdown("---")

            with st.expander("Returning Flights"):
                for flight in itinerary.transportation.returning_flights:
                    st.markdown(f"**{flight.airline}**: {flight.from_airport} ➡️ {flight.to_airport}")
                    st.write(f"Departure: {flight.departure_time} | Arrival: {flight.arrival_time}")
                    st.write(f"Duration: {flight.duration} | Price: {flight.price} {flight.currency or ''}")
                    st.markdown("---")

        st.header("🏨 Hotel Recommendations")
        if itinerary.hotels:
            for hotel in itinerary.hotels:
                st.markdown(f"### {hotel.hotel_name}")
                st.write(f"Dates: {hotel.check_in_date} → {hotel.check_out_date} ({hotel.duration})")
                st.write(f"Price: {hotel.total_price} {hotel.currency} ({hotel.per_day_price}/day)")
                st.write(f"Guests: {hotel.guests}")
                st.markdown("---")

        st.header("📅 AI Itinerary Plan")
        if itinerary.llm_plan:
            st.markdown(itinerary.llm_plan)

        st.header("🎯 Activities")
        if itinerary.activities:
            st.write(itinerary.activities)

        st.header("🌤️ Weather Forecast")
        if itinerary.weather:
            st.write(itinerary.weather)

        st.header("💰 Budget Estimate")
        if itinerary.budget_estimate:
            b = itinerary.budget_estimate
            st.json({
                "Flights": b.transportation_cost,
                "Hotels": b.hotel_cost,
                "Activities": b.activities_cost,
                "Food": b.food_estimate,
                "Local Travel": b.internal_travel_cost,
                "Misc": b.miscellaneous_cost,
                "Total": b.total_cost,
                "Per Person": b.per_person_cost
            })



        