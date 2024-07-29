# Import the Streamlit library for creating interactive web applications
import streamlit as st
import os  # Import the OS module for operating system-related functions, primarily for environment variables
# Import the Google Generative AI library for interacting with AI models
import google.generativeai as genai
import requests
import base64  # Import the base64 library for encoding binary data as text

# Configure the API key
# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
genai.configure(api_key='AIzaSyAvIGT2oKJmw-OHEM18o8VODzds_D2a5rk')

# model instance for generating text
model = genai.GenerativeModel('gemini-pro')

# Function for generating content from LLM model
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

def generate_trip_plan(duration, destination, style):
    prompt = f"Create a {duration}-day trip itinerary for {destination} focusing on {style} travel. Include daily activities, must-see attractions, and accommodation suggestions."
    response = model.generate_content(prompt)
    trip_plan = response.text
    return trip_plan

# Function to fetch data from Google Places API
def fetch_local_attractions(destination):
    api_key = 'AIzaSyCBBA_s8jd6eYXr3Q88nc92N5l3ilYRBHs'
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=tourist+attractions+in+{destination}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        attractions = data.get('results', [])
        return attractions
    else:
        return []

# Function to generate trip plan with additional data
def enhanced_trip_plan(duration, destination, style):
    trip_plan = generate_trip_plan(duration, destination, style)
    attractions = fetch_local_attractions(destination)
    
    if attractions:
        trip_plan += "\n\nMust-See Attractions:\n"
        for attraction in attractions:
            trip_plan += f"- {attraction['name']} (Rating: {attraction.get('rating', 'N/A')})\n"
    
    return trip_plan

# Streamlit app
st.set_page_config(page_title='AI Trip Planner')

# Header
st.header('AI Trip Planner by VAIBHAV')

# Create input fields for trip preferences
duration = st.number_input('Trip Duration (days)', min_value=1, step=1)
destination = st.text_input('Trip Destination')
style = st.selectbox('Trip Style', ['Adventure', 'Relaxation', 'Cultural'])

# Create a button to trigger trip plan generation
submit = st.button('Generate Trip Plan')

# Generate and display the trip plan if the button is clicked
trip_plan = None
if submit:
    trip_plan = enhanced_trip_plan(duration, destination, style)
    
if trip_plan:
    st.subheader('Your Trip Plan')
    st.write(trip_plan)