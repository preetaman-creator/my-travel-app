import streamlit as st
from google.genai import Client
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Humble Travels", page_icon="🌎", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white; border-radius: 12px; padding: 12px; width: 100%;
    }
    .itinerary-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px; border-left: 5px solid #00f2fe; margin-top: 20px;
    }
    h1 { text-align: center; color: #00f2fe; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    model_choice = st.selectbox("Model", ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"])

# --- MAIN UI ---
st.title("🌎 AI Travel Designer")

col1, col2 = st.columns(2)

with col1:
    location = st.text_input("Destination", placeholder="e.g. Dubai")
    days = st.slider("Days", 1, 14, 3)

with col2:
    categories = st.multiselect(
        "Interests",
        ["Luxury", "Food", "Adventure", "History", "Relaxation"],
        default=["Luxury"]
    )

if st.button("Build My Journey"):
    if not api_key:
        st.error("Please provide your API key in the sidebar.")
    else:
        try:
            # Initialize the Client directly
            client = Client(api_key=api_key)
            
            prompt = f"Create a {days}-day itinerary for {location} focusing on {', '.join(categories)}."
            
            with st.spinner("Designing..."):
                response = client.models.generate_content(
                    model=model_choice,
                    contents=prompt
                )
                
                st.markdown("---")
                st.markdown(f'<div class="itinerary-card">{response.text}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {e}")
