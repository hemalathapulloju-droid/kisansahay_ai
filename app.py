import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="KisanSense Platform",
    page_icon="🌾",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "farmer_name" not in st.session_state:
    st.session_state.farmer_name = ""

if "language" not in st.session_state:
    st.session_state.language = "English"

# =====================================================
# LOGIN PAGE
# =====================================================
def login_page():
    st.markdown("# 🌾 KisanSense")
    st.markdown("### Farmer Login")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Farmer Name")
        village = st.text_input("Village")

    with col2:
        phone = st.text_input("Mobile Number")
        language = st.selectbox(
            "Preferred Language",
            ["English", "Telugu", "Hindi", "Tamil"]
        )

    if st.button("Login"):
        if name:
            st.session_state.logged_in = True
            st.session_state.farmer_name = name
            st.session_state.language = language
            st.rerun()
        else:
            st.warning("Please enter your name")

# =====================================================
# AI ADVISORY LOGIC
# =====================================================
def agri_advice(query, lang):
    q = query.lower()

    responses = {
        "aphid": {
            "English": "Apply Neem oil 3–5 ml per litre. Avoid excess nitrogen.",
            "Telugu": "నీమ్ ఆయిల్ 3–5 మి.లీ లీటర్ నీటిలో పిచికారీ చేయాలి.",
            "Hindi": "नीम तेल 3–5 मि.ली. प्रति लीटर पानी में छिड़कें।",
            "Tamil": "நீம் எண்ணெய் 3–5 மி.லி. தெளிக்கவும்."
        }
    }

    if "aphid" in q:
        return responses["aphid"][lang]

    return {
        "English": "Please consult your local agriculture officer.",
        "Telugu": "స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి.",
        "Hindi": "स्थानीय कृषि अधिकारी से संपर्क करें।",
        "Tamil": "உள்ளூர் வேளாண் அதிகாரியை அணுகவும்."
    }[lang]

# =====================================================
# DASHBOARD
# =====================================================
def dashboard():

    # ---------------- SIDEBAR ----------------
    st.sidebar.title("🌾 KisanSense")

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

    st.sidebar.markdown("---")
    st.sidebar.write(f"Logged in as: **{st.session_state.farmer_name}**")
    st.sidebar.write(f"Language: **{st.session_state.language}**")

    # =====================================================
    # MAIN CONTENT
    # =====================================================

    st.markdown(f"## Welcome, {st.session_state.farmer_name} 👋")
    st.divider()

    # ---------------- DASHBOARD HOME ----------------
    if page == "🏠 Dashboard":
        col1, col2, col3 = st.columns(3)

        col1.success("🌱 Crop Advisory")
        col2.info("🐛 Disease Detection")
        col3.warning("🤖 AI Assistant")

        st.markdown("### Platform Overview")
        st.write(
            "KisanSense integrates AI advisory, crop insights, government schemes, "
            "and weather guidance into one farmer-centric platform."
        )

    # ---------------- AI ASSISTANT ----------------
    if page == "🤖 AI Assistant":
        st.header("🤖 AI Assistant")

        if "chat" not in st.session_state:
            st.session_state.chat = []

        query = st.chat_input("Ask your farming question...")

        if query:
            st.session_state.chat.append(("user", query))
            reply = agri_advice(query, st.session_state.language)
            st.session_state.chat.append(("assistant", reply))

        for role, msg in st.session_state.chat:
            if role == "user":
                st.chat_message("user").write(msg)
            else:
                st.chat_message("assistant").write(msg)

    # ---------------- CROP RECOMMENDATION ----------------
    if page == "🌱 Crop Recommendation":
        st.header("🌱 Recommended Crops")
        st.success("Based on region & season: Rice, Pulses, Millets")

    # ---------------- DISEASE DETECTION ----------------
    if page == "📸 Disease Detection":
        st.header("📸 Crop Disease Detection")
        st.file_uploader("Upload crop leaf image")
        st.info("AI-based detection module ready for integration")

    # ---------------- GOVERNMENT SCHEMES ----------------
    if page == "🏛 Government Schemes":
        st.header("🏛 Government Schemes")
        st.write("• PM-Kisan – ₹6000 per year")
        st.write("• PMFBY Crop Insurance")
        st.write("• State-level fertilizer subsidy programs")

    # ---------------- WEATHER ----------------
    if page == "🌦 Weather & Advisory":
        st.header("🌦 Weather & Advisory")
        st.warning("Rain expected tomorrow. Avoid pesticide spraying.")

    # ---------------- NOTIFICATIONS ----------------
    if page == "🔔 Notifications":
        st.header("🔔 Notifications")
        st.info("No new notifications")

    # ---------------- ABOUT ----------------
    if page == "ℹ️ About":
        st.header("ℹ️ About KisanSense")
        st.write(
            "KisanSense is a multilingual agritech platform combining AI advisory, "
            "farmer profiles, crop insights, and rural accessibility."
        )

    # ---------------- CONTACT ----------------
    if page == "📞 Contact":
        st.header("📞 Contact Us")
        st.write("Email: support@kisansense.ai")
        st.write("Helpline: 1800-000-000")

# =====================================================
# MAIN
# =====================================================
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()
