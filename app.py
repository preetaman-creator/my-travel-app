import streamlit as st

# --- 1. PRE-FLIGHT CHECK (Fixes the Module Error) ---
try:
    from google import genai
except ImportError:
    st.error("⏳ The AI engine is still being installed by the server. Please wait 60 seconds and then refresh this page!")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Humble Travels", page_icon="🌎", layout="wide")

# Modern Dark UI Styling
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white; border-radius: 12px; font-weight: bold; height: 50px;
    }
    .itinerary-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 20px; border-left: 6px solid #00f2fe; margin-top: 20px;
    }
    h1 { color: #00f2fe; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR SETUP ---
with st.sidebar:
    st.title("⚙️ Setup")
    api_key = st.text_input("Paste Gemini API Key", type="password")
    # UPDATED 2026 MODEL NAMES
    model_choice = st.selectbox("Select Model", [
        "gemini-3.1-pro-preview", 
        "gemini-3-flash-preview",
        "gemini-2.0-flash"
    ])
    st.info("💡 Paid users should use 'gemini-3.1-pro-preview' for best results.")

st.title("🌎 AI Travel Designer")

# --- 4. USER INPUTS ---
col1, col2 = st.columns(2)
with col1:
    location = st.text_input("Where are you going?", placeholder="e.g. Dubai, UAE")
    days = st.slider("Number of Days", 1, 14, 3)
with col2:
    categories = st.multiselect("Your Travel Style", 
                                ["Luxury", "Foodie", "Adventure", "History", "Family"], 
                                default=["Luxury"])

# --- 5. BUILD JOURNEY ---
if st.button("Build My Journey"):
    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar.")
    else:
        try:
            # Connect using the 2026 Client standard
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            Create a professional {days}-day travel itinerary for {location}.
            Style: {', '.join(categories)}.
            Please include specific high-end recommendations and a 'Local Secret' for each day.
            Format with bold headers.
            """
            
            with st.spinner("Building your custom itinerary..."):
                # Call the model
                response = client.models.generate_content(
                    model=model_choice,
                    contents=prompt
                )
                
                st.markdown("---")
                st.markdown(f'<div class="itinerary-box">{response.text}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            # If it still 404s, we show a helpful tip
            if "404" in str(e):
                st.error("Model Error: The selected model name is not recognized. Try switching to 'gemini-3-flash-preview' in the sidebar.")
            else:
                st.error(f"Something went wrong: {e}")
