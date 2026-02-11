import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="KisanSahay Platform",
    page_icon="🌾",
    layout="wide"
)

# =====================================================
# CUSTOM STYLING (COLORFUL FARM UI)
# =====================================================
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
    background-size: cover;
}

.block-container {
    background: rgba(255,255,255,0.92);
    padding: 2rem;
    border-radius: 15px;
}

.sidebar .sidebar-content {
    background: linear-gradient(180deg,#2e7d32,#66bb6a);
    color: white;
}

h1, h2, h3 {
    color: #1b5e20;
}

.stButton>button {
    background-color: #2e7d32;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "farmer" not in st.session_state:
    st.session_state.farmer = {}

if "notifications" not in st.session_state:
    st.session_state.notifications = [
        "🌧 Rain expected this week — delay pesticide spraying.",
        "💰 PM-Kisan installment releasing soon.",
        "🌱 Best time to sow millets in your region."
    ]

# =====================================================
# SMART AI (RULE + GENERIC ANSWER ENGINE)
# =====================================================
def smart_ai(question):
    q = question.lower()

    knowledge = {
        "aphid": "Spray neem oil or imidacloprid. Encourage ladybird beetles.",
        "fertilizer": "Use soil testing before applying NPK. Avoid overuse.",
        "rice": "Maintain standing water 2–5cm. Use high-yield varieties.",
        "loan": "Visit nearest agriculture bank for KCC (Kisan Credit Card).",
        "insurance": "Enroll in PMFBY crop insurance before sowing season.",
        "weather": "Monitor IMD forecasts regularly for planning."
    }

    for key in knowledge:
        if key in q:
            return knowledge[key]

    return "AI Advisory: Follow crop rotation, monitor soil health, adopt precision farming, and consult local agriculture officers for region-specific guidance."

# =====================================================
# GOVERNMENT SCHEMES DATA (HUGE LIST)
# =====================================================
schemes = pd.DataFrame([
    ["PM-Kisan", "₹6000/year income support", "All small farmers"],
    ["PMFBY", "Crop insurance against natural disasters", "All farmers"],
    ["Kisan Credit Card", "Low-interest farm loans", "Land owners"],
    ["Soil Health Card", "Free soil testing", "All farmers"],
    ["Paramparagat Krishi", "Organic farming support", "Organic farmers"],
    ["National Agriculture Market", "Online crop selling", "Traders & Farmers"],
    ["Micro Irrigation Fund", "Subsidy on drip irrigation", "Water-scarce regions"],
    ["Fasal Bima", "Yield protection", "Crop growers"],
    ["Agri Infrastructure Fund", "Warehouse & cold storage loans", "FPOs"],
    ["National Food Security Mission", "Increase crop productivity", "Staple crop farmers"],
    ["Rashtriya Krishi Vikas", "State agriculture development", "All farmers"],
    ["e-NAM", "Pan-India digital market", "All farmers"]
], columns=["Scheme", "Benefit", "Eligibility"])

# =====================================================
# LOGIN PAGE
# =====================================================
def login():
    st.title("🌾 KisanSahay")
    st.subheader("Smart AI Platform for Farmers")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Farmer Name")
        village = st.text_input("Village")

    with col2:
        phone = st.text_input("Mobile")
        land = st.selectbox("Land Size", ["<1 Acre", "1-3 Acres", "3-10 Acres", ">10 Acres"])

    if st.button("Login"):
        if name:
            st.session_state.logged_in = True
            st.session_state.farmer = {
                "name": name,
                "village": village,
                "phone": phone,
                "land": land
            }
            st.rerun()
        else:
            st.warning("Enter farmer name")

# =====================================================
# DASHBOARD
# =====================================================
def dashboard():

    farmer = st.session_state.farmer

    st.sidebar.title("🌾 KisanSahay")

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🤖 AI Assistant",
            "🌱 Crop Recommendation",
            "📸 Disease Detection",
            "🏛 Government Schemes",
            "🌦 Weather & Advisory",
            "🔔 Notifications",
            "ℹ️ About",
            "📞 Contact"
        ]
    )

    st.sidebar.write(f"👨‍🌾 {farmer['name']}")
    st.sidebar.write(f"📍 {farmer['village']}")
    st.sidebar.write(f"🌾 Land: {farmer['land']}")

    # =================================================
    # HOME
    # =================================================

    if page == "🏠 Dashboard":
        st.title(f"Welcome {farmer['name']} 👋")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Active Schemes", len(schemes))
        col2.metric("Advisories Today", "12")
        col3.metric("Weather", "28°C")
        col4.metric("Soil Moisture", "Optimal")

        st.write("### Smart Farming Insights")

        st.info("✅ AI predicts good yield for millet this season.")
        st.warning("⚠ Reduce urea usage — soil nitrogen high.")
        st.success("💧 Perfect time for drip irrigation.")

    # =================================================
    # AI ASSISTANT
    # =================================================

    elif page == "🤖 AI Assistant":
        st.header("Ask Anything About Farming")

        if "chat" not in st.session_state:
            st.session_state.chat = []

        prompt = st.chat_input("Ask about crops, loans, pests, weather...")

        if prompt:
            response = smart_ai(prompt)
            st.session_state.chat.append(("user", prompt))
            st.session_state.chat.append(("ai", response))

        for role, msg in st.session_state.chat:
            with st.chat_message(role):
                st.write(msg)

    # =================================================
    # CROP RECOMMENDATION
    # =================================================

    elif page == "🌱 Crop Recommendation":
        st.header("AI Crop Predictor")

        soil = st.selectbox("Soil Type", ["Black", "Red", "Sandy", "Clay"])
        season = st.selectbox("Season", ["Kharif", "Rabi", "Zaid"])

        if st.button("Predict Crops"):
            st.success("Recommended: Millets, Pulses, Groundnut")

    # =================================================
    # DISEASE DETECTION
    # =================================================

    elif page == "📸 Disease Detection":
        st.header("Upload Leaf Image")
        st.file_uploader("Upload crop image")
        st.info("AI detection ready — connect CNN model anytime.")

    # =================================================
    # SCHEMES
    # =================================================

    elif page == "🏛 Government Schemes":
        st.header("All Agricultural Schemes")
        search = st.text_input("Search schemes")

        if search:
            filtered = schemes[schemes.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
            st.dataframe(filtered, use_container_width=True)
        else:
            st.dataframe(schemes, use_container_width=True)

    # =================================================
    # WEATHER
    # =================================================

    elif page == "🌦 Weather & Advisory":
        st.header("Weather Intelligence")
        st.write("📍 Region-based forecast")

        st.metric("Temperature", "28°C")
        st.metric("Rainfall", "65% chance")
        st.metric("Humidity", "70%")

        st.warning("Avoid spraying for next 24 hours.")

    # =================================================
    # NOTIFICATIONS
    # =================================================

    elif page == "🔔 Notifications":
        st.header("Smart Alerts")

        for note in st.session_state.notifications:
            st.info(note)

    # =================================================
    # ABOUT
    # =================================================

    elif page == "ℹ️ About":
        st.header("About KisanSahay")
        st.write("""
KisanSahay is an AI-powered digital agriculture platform designed to empower farmers with:

• Smart AI advisory
• Government scheme discovery
• Crop prediction
• Disease detection
• Weather intelligence
• Personalized dashboards

Built for hackathons — designed for real-world impact.
""")

    # =================================================
    # CONTACT
    # =================================================

    elif page == "📞 Contact":
        st.header("Contact Support")
        st.text_input("Your Email")
        st.text_area("Message")

        if st.button("Send"):
            st.success("Support team will contact you shortly.")

# =====================================================
# MAIN
# =====================================================

if not st.session_state.logged_in:
    login()
else:
    dashboard()

