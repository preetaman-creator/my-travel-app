import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="Humble Travels", page_icon="🌎", layout="wide")

# --- CUSTOM CSS FOR ATTRACTIVE UI ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white; border: none; border-radius: 10px;
        padding: 10px 24px; font-weight: bold; width: 100%;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #1c1f26; color: white; border-radius: 8px; border: 1px solid #4facfe;
    }
    .itinerary-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px; border-left: 5px solid #00f2fe; margin-bottom: 20px;
    }
    h1 { text-align: center; background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR SETUP ---
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    model_choice = st.selectbox("Choose Model", ["gemini-1.5-pro", "gemini-1.5-flash"])

# --- MAIN UI ---
st.title("🌎 AI Travel Designer")
st.markdown("<p style='text-align: center;'>Bespoke itineraries generated in seconds.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    location = st.text_input("Destination", placeholder="e.g. Amalfi Coast, Italy")
    days = st.slider("Duration (Days)", 1, 14, 3)

with col2:
    categories = st.multiselect(
        "Focus Areas",
        ["Luxury & Fine Dining", "Hidden Gems", "Adventure & Trekking", "History & Architecture", "Relaxation"],
        default=["Luxury & Fine Dining"]
    )

if st.button("Build My Journey"):
    if not api_key:
        st.error("Please provide your API key in the sidebar.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_choice)
            
            prompt = f"""
            Create a professional, high-end {days}-day travel itinerary for {location}.
            Preferences: {', '.join(categories)}.
            Format with bold headers for each day. For each day, include:
            - Morning, Afternoon, Evening activities.
            - A 'Pro-Tip' section for that specific day.
            Use professional, sophisticated language.
            """
            
            with st.spinner("Designing your bespoke experience..."):
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(f"### 📍 Itinerary for {location}")
                # Wrapping output in a styled div
                st.markdown(f'<div class="itinerary-card">{response.text}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
