import streamlit as st

# --- CRITICAL FIX FOR THE ERROR ---
try:
    from google import genai
except ImportError:
    st.error("The 'Google GenAI' library is still being installed by the server. Please wait 60 seconds and refresh the page!")
    st.stop()

# --- APP SETUP ---
st.set_page_config(page_title="Humble Travels", page_icon="🌎", layout="wide")

# UI Styling
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white; border-radius: 12px; font-weight: bold; border: none;
    }
    .itinerary-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px; border-left: 5px solid #00f2fe; margin-top: 20px;
    }
    h1 { color: #00f2fe; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for Key
with st.sidebar:
    st.title("⚙️ Setup")
    api_key = st.text_input("Paste Gemini API Key", type="password")
    # Recommended models for 2026
    model_choice = st.selectbox("Model", ["gemini-3.1-pro", "gemini-3.1-flash"])

st.title("🌎 AI Travel Designer")

# Inputs
col1, col2 = st.columns(2)
with col1:
    location = st.text_input("Where to?", placeholder="e.g. Dubai")
    days = st.slider("Days", 1, 14, 3)
with col2:
    categories = st.multiselect("Your Style", ["Luxury", "Foodie", "Adventure", "History"], default=["Luxury"])

# Build Button
if st.button("Build My Journey"):
    if not api_key:
        st.warning("You need to paste your API Key in the sidebar first!")
    else:
        try:
            # The 2026 standard way to connect
            client = genai.Client(api_key=api_key)
            
            prompt = f"Create a {days}-day itinerary for {location} with focus on {', '.join(categories)}."
            
            with st.spinner("Designing your experience..."):
                response = client.models.generate_content(
                    model=model_choice,
                    contents=prompt
                )
                st.markdown("---")
                st.markdown(f'<div class="itinerary-box">{response.text}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Execution Error: {e}")
