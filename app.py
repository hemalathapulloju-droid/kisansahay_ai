import streamlit as st
import requests
from deep_translator import GoogleTranslator
import base64
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="KisanSahay",
    layout="wide",
    page_icon="🌾"
)

# ================= BACKGROUND =================
def add_bg():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(
                rgba(0,0,0,0.75),
                rgba(0,0,0,0.75)
            ),
            url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
            background-size: cover;
        }}

        h1, h2, h3, h4, h5, h6, p, label {{
            color: white !important;
        }}

        .css-1d391kg {{
            background-color: rgba(0,0,0,0.85);
        }}

        .stButton>button {{
            background-color: #2ecc71;
            color: white;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg()

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "applied_schemes" not in st.session_state:
    st.session_state.applied_schemes = []

# ================= LOGIN =================
def login():

    st.title("🌾 Welcome to KisanSahay")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Farmer Name")
        place = st.text_input("Village / City")
        land = st.selectbox("Land Size", ["<1 Acre", "1-3 Acres", "3-5 Acres", "5+ Acres"])

    with col2:
        phone = st.text_input("Mobile Number")
        language = st.selectbox("Preferred Language",
                                ["English", "Telugu", "Hindi", "Marathi", "Tamil"])

    if st.button("Login"):

        if name and place:
            st.session_state.logged_in = True
            st.session_state.name = name
            st.session_state.place = place
            st.session_state.land = land
            st.session_state.language = language
            st.rerun()

        else:
            st.warning("Please fill required details")


# ================= AI CHAT =================
def ai_chatbot():

    st.header("🤖 Smart AI Assistant")

    query = st.text_input("Ask anything about crops, diseases, schemes...")

    # VOICE INPUT
    audio = st.file_uploader("🎤 Upload Voice Question", type=["wav","mp3"])

    if audio:
        st.info("Voice received — converting to text requires Whisper API (optional).")

    if query:

        # translate to english
        translated = GoogleTranslator(source='auto', target='en').translate(query)

        # SIMPLE INTELLIGENT RESPONSES
        if "scheme" in translated.lower():
            response = "You can explore PM-KISAN, PMFBY crop insurance, Soil Health Card, and KCC loans."

        elif "disease" in translated.lower():
            response = "Upload the crop image in Disease Detection for AI diagnosis."

        elif "fertilizer" in translated.lower():
            response = "Use balanced NPK fertilizers and always conduct soil testing."

        else:
            # OPTIONAL LLM CALL
            HF_KEY = st.secrets.get("HF_API_KEY", "")

            if HF_KEY:

                API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

                headers = {"Authorization": f"Bearer {HF_KEY}"}

                payload = {"inputs": translated}

                res = requests.post(API_URL, headers=headers, json=payload)

                try:
                    response = res.json()[0]["generated_text"]
                except:
                    response = "AI is learning — please try again."

            else:
                response = "AI key missing. Add HF_API_KEY in secrets."

        # translate back
        final = GoogleTranslator(source='en', target='auto').translate(response)

        st.success(final)


# ================= WEATHER =================
def weather():

    st.header("🌦 Real-Time Weather")

    API_KEY = st.secrets.get("WEATHER_KEY","")

    if not API_KEY:
        st.warning("Add WEATHER_KEY in secrets.")
        return

    city = st.session_state.place

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    res = requests.get(url).json()

    if res.get("main"):

        temp = res["main"]["temp"]
        humidity = res["main"]["humidity"]
        desc = res["weather"][0]["description"]

        st.metric("Temperature", f"{temp}°C")
        st.metric("Humidity", f"{humidity}%")
        st.info(desc)

    else:
        st.error("Weather not found.")


# ================= DISEASE DETECTION =================
def disease():

    st.header("📸 AI Plant Disease Detection")

    file = st.file_uploader("Upload Leaf Image", type=["jpg","png"])

    if file:

        HF_KEY = st.secrets.get("HF_API_KEY","")

        if not HF_KEY:
            st.warning("Add HF_API_KEY in secrets.")
            return

        API_URL = "https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"

        headers = {"Authorization": f"Bearer {HF_KEY}"}

        res = requests.post(API_URL, headers=headers, data=file.read())

        try:
            prediction = res.json()[0]["label"]

            st.success(f"Disease Detected: {prediction}")

            st.write("### Recommended Action:")
            st.write("- Remove infected leaves")
            st.write("- Apply neem oil")
            st.write("- Avoid overwatering")

        except:
            st.error("Could not detect. Try clearer image.")


# ================= SCHEMES =================
def schemes():

    st.header("🏛 Government Schemes")

    scheme_data = [

        {
            "name":"PM-KISAN",
            "eligibility":"All small & marginal farmers",
            "benefit":"₹6000 per year",
            "link":"https://pmkisan.gov.in/"
        },

        {
            "name":"PMFBY Crop Insurance",
            "eligibility":"Farmers growing notified crops",
            "benefit":"Insurance against crop loss",
            "link":"https://pmfby.gov.in/"
        },

        {
            "name":"Kisan Credit Card",
            "eligibility":"Farmers with land",
            "benefit":"Low-interest loans",
            "link":"https://www.myscheme.gov.in/schemes/kcc"
        },

        {
            "name":"Soil Health Card",
            "eligibility":"All farmers",
            "benefit":"Free soil testing",
            "link":"https://soilhealth.dac.gov.in/"
        }
    ]

    for s in scheme_data:

        with st.container():

            st.subheader(s["name"])
            st.write(f"✅ Eligibility: {s['eligibility']}")
            st.write(f"💰 Benefit: {s['benefit']}")

            col1, col2 = st.columns(2)

            if col1.button(f"Apply for {s['name']}"):
                st.session_state.applied_schemes.append(s["name"])
                st.success("Application tracked!")

                st.markdown(f"[CLICK HERE TO APPLY]({s['link']})")

    st.divider()

    st.subheader("📊 Application Tracking")

    if st.session_state.applied_schemes:
        for a in st.session_state.applied_schemes:
            st.write(f"🟢 {a} — In Progress")

    else:
        st.info("No schemes applied yet.")


# ================= DASHBOARD =================
def dashboard():

    st.title(f"Welcome {st.session_state.name} 👋")

    col1, col2, col3 = st.columns(3)

    col1.success("🌱 Crop Advisory Ready")
    col2.info("🤖 AI Enabled")
    col3.warning("🌦 Live Weather Active")

    st.write("KisanSahay — AI Powered Farming Platform")


# ================= SIDEBAR =================
def main_app():

    st.sidebar.title("🌾 KisanSahay")

    page = st.sidebar.radio("Navigation", [

        "🏠 Dashboard",
        "🤖 AI Assistant",
        "📸 Disease Detection",
        "🏛 Government Schemes",
        "🌦 Weather & Advisory",
        "🔔 Notifications",
        "ℹ️ About",
        "📞 Contact"
    ])

    st.sidebar.write(f"👤 {st.session_state.name}")
    st.sidebar.write(f"📍 {st.session_state.place}")
    st.sidebar.write(f"🌾 {st.session_state.land}")

    if page == "🏠 Dashboard":
        dashboard()

    elif page == "🤖 AI Assistant":
        ai_chatbot()

    elif page == "📸 Disease Detection":
        disease()

    elif page == "🏛 Government Schemes":
        schemes()

    elif page == "🌦 Weather & Advisory":
        weather()

    elif page == "🔔 Notifications":
        st.info("No new alerts")

    elif page == "ℹ️ About":
        st.write("KisanSahay is an AI-driven smart farming platform helping farmers make better decisions.")

    elif page == "📞 Contact":
        st.write("📞 +91 9059184778")
        st.write("📧 kisansahayfarm@gmail.com")


# ================= RUN =================
if not st.session_state.logged_in:
    login()
else:
    main_app()




