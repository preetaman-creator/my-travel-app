import streamlit as st
from google import genai
from google.genai import types

# --- PAGE CONFIG ---
st.set_page_config(page_title="Humble Travels", page_icon="🌎", layout="wide")

# --- MODERN STYLING (Humble Accounting Brand Vibes) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white; border: none; border-radius: 12px;
        padding: 12px 24px; font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); opacity: 0.9; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #1c1f26; color: white; border-radius: 10px; border: 1px solid #4facfe;
    }
    .itinerary-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 25px; border-radius: 20px; border-left: 6px solid #00f2fe;
        line-height: 1.6; margin-top: 20px;
    }
    h1 { text-align: center; font-weight: 800; color: #00f2fe; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Since you are on the paid tier, 'Gemini 3.1 Pro' is recommended for detailed itineraries.")
    model_choice = st.selectbox("Model", ["gemini-3.1-pro", "gemini-3.1-flash"])

# --- APP INTERFACE ---
st.title("🌎 AI Travel Designer")
st.markdown("<p style='text-align: center; color: #888;'>Create precision itineraries based on your preferences.</p>", unsafe_allow_html=True)

# Layout Columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    location = st.text_input("Destination", placeholder="e.g. Dubai, UAE")
    days = st.slider("Duration (Days)", 1, 14, 3)

with col2:
    categories = st.multiselect(
        "Focus Areas",
        ["Luxury & Fine Dining", "Hidden Gems", "Adventure & Trekking", "History & Architecture", "Relaxation", "Family Friendly"],
        default=["Luxury & Fine Dining", "History & Architecture"]
    )

if st.button("Build My Journey"):
    if not api_key:
        st.warning("Please paste your API Key in the sidebar to begin.")
    else:
        try:
            # Initialize Client using the 2026 google-genai SDK
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            Act as a high-end travel consultant. Create a detailed {days}-day itinerary for {location}.
            Target Interests: {', '.join(categories)}.
            
            Requirements:
            1. Organized by Day (Day 1, Day 2, etc.).
            2. For each day, provide a Morning, Afternoon, and Evening plan.
            3. Include a 'Financial Tip' or 'CPA Pro-Tip' for each location (e.g., VAT refunds, best currency practices, or booking efficiency).
            4. Suggest specific restaurants that match the 'Fine Dining' or 'Local' focus.
            
            Keep the tone professional, crisp, and detail-oriented.
            """
            
            with st.spinner("Analyzing destination data and building your plan..."):
                response = client.models.generate_content(
                    model=model_choice,
                    contents=prompt
                )
                
                st.markdown("---")
                st.success(f"Successfully generated itinerary for {location}!")
                st.markdown(f'<div class="itinerary-card">{response.text}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Check if your API Key is active and you have selected a model available in your region.")
