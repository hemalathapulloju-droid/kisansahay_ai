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

        query = st.chat_input("Ask your farming
