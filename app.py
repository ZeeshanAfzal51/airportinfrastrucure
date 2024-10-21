import streamlit as st
import requests

# Set up the AviationStack API key and base URL
API_KEY = st.secrets["api"]["aviationstack_key"]
BASE_URL = 'https://api.aviationstack.com/v1/flights'

# Function to get flight details
def get_flight_details(flight_number):
    params = {
        'access_key': API_KEY,
        'flight_iata': flight_number  # Flight number (IATA code)
    }
    
    response = requests.get(BASE_URL, params=params)
    flight_data = response.json()
    
    if 'data' in flight_data and flight_data['data']:
        return flight_data['data'][0]
    else:
        return None

# Streamlit app UI
st.title("Flight Arrival Time Tracker")

# Input from the user (Flight number)
flight_number = st.text_input("Enter Flight Number (IATA format)", "")

if flight_number:
    st.write(f"Looking up flight details for: **{flight_number}**")
    
    # Fetch flight details
    flight_info = get_flight_details(flight_number)
    
    if flight_info:
        airline = flight_info['airline']['name']
        departure_airport = flight_info['departure']['airport']
        arrival_airport = flight_info['arrival']['airport']
        scheduled_arrival = flight_info['arrival']['scheduled']
        estimated_arrival = flight_info['arrival']['estimated']
        actual_arrival = flight_info['arrival'].get('actual', 'N/A')
        
        # Display flight details
        st.subheader(f"Flight Details for {flight_number}")
        st.write(f"**Airline**: {airline}")
        st.write(f"**From**: {departure_airport}")
        st.write(f"**To**: {arrival_airport}")
        st.write(f"**Scheduled Arrival Time**: {scheduled_arrival}")
        st.write(f"**Estimated Arrival Time**: {estimated_arrival}")
        st.write(f"**Actual Arrival Time**: {actual_arrival}")
    else:
        st.error("No flight information found. Please check the flight number.")
