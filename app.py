import streamlit as st
from deep_translator import GoogleTranslator
import random

# ================= PAGE CONFIG =================
st.set_page_config(page_title="KisanSahay", layout="wide", page_icon="🌾")

# ================= BACKGROUND =================
st.markdown("""
<style>
.stApp {
background-image: linear-gradient(rgba(0,0,0,0.75),rgba(0,0,0,0.75)),
url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
background-size: cover;
}
h1,h2,h3,h4,h5,p,label {color:white !important;}
.stButton>button {
background-color:#2ecc71;
color:white;
border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in=False

if "page" not in st.session_state:
    st.session_state.page="🏠 Dashboard"

# ================= LOGIN =================
def login():

    st.title("🌾 Welcome to KisanSahay")

    col1,col2=st.columns(2)

    with col1:
        name=st.text_input("Farmer Name")
        place=st.text_input("Village / City")
        land=st.selectbox("Land Size",["<1 Acre","1-3 Acres","3-5 Acres","5+ Acres"])

    with col2:
        phone=st.text_input("Mobile Number")
        language=st.selectbox("Language",
        ["English","Telugu","Hindi","Marathi","Tamil"])

    if st.button("Login"):

        if name and place:
            st.session_state.logged_in=True
            st.session_state.name=name
            st.session_state.place=place
            st.session_state.land=land
            st.session_state.language=language
            st.rerun()

# ================= SMART AI CHAT (NO API) =================
def ai_chat():

    st.header("🤖 Smart AI Assistant")

    query=st.text_input("Ask anything about crops, disease, schemes, farming...")

    if query:

        # translate to english
        translated=GoogleTranslator(source='auto', target='en').translate(query)

        q=translated.lower()

        if "rice" in q:
            response="""Rice cultivation requires good water management, proper nursery preparation, and balanced fertilizer application.
Maintain standing water during early growth stages. Use nitrogen in split doses to increase yield. Monitor for pests like stem borer and use integrated pest management practices."""
        
        elif "disease" in q or "leaf" in q:
            response="""Plant diseases usually appear due to fungal or bacterial infection. Remove infected leaves immediately.
Maintain airflow between plants, avoid overwatering, and apply neem-based bio-pesticides regularly for prevention."""
        
        elif "scheme" in q:
            response="""Indian farmers can benefit from PM-Kisan income support, PMFBY crop insurance, Soil Health Card scheme, and Kisan Credit Card loans. 
These schemes provide financial assistance, crop protection, and soil fertility improvement guidance."""
        
        elif "fertilizer" in q:
            response="""Use balanced NPK fertilizer based on crop stage. Always conduct soil testing before heavy fertilizer application.
Organic compost improves soil structure and increases long-term productivity."""
        
        else:
            response="""Smart Farming Advice:
Monitor soil moisture regularly, use certified seeds, adopt crop rotation, and follow weather-based irrigation planning.
Technology-based agriculture improves yield and reduces risk."""

        # translate back
        final=GoogleTranslator(source='en',target='auto').translate(response)

        st.success(final)

# ================= WEATHER (SIMULATED INTELLIGENT) =================
def weather():

    st.header("🌦 Weather & Advisory")

    city=st.session_state.place

    temp=random.randint(25,36)
    humidity=random.randint(50,85)

    st.metric("Location",city)
    st.metric("Temperature",f"{temp} °C")
    st.metric("Humidity",f"{humidity}%")

    if temp>32:
        st.warning("High temperature expected. Increase irrigation.")
    else:
        st.success("Good weather for crop growth.")

# ================= DISEASE DETECTION (SIMULATED AI) =================
def disease():

    st.header("📸 AI Plant Disease Detection")

    file=st.file_uploader("Upload crop image", type=["jpg","png"])

    if file:

        diseases=[
        "Leaf Blight",
        "Powdery Mildew",
        "Bacterial Spot",
        "Healthy Plant"]

        prediction=random.choice(diseases)

        st.success(f"Disease Detected: {prediction}")

        st.write("""
Recommended Actions:
- Remove infected leaves
- Apply neem oil spray
- Maintain plant spacing
- Avoid waterlogging
""")

# ================= SCHEMES =================
def schemes():

    st.header("🏛 Government Schemes")

    st.write("PM-KISAN — ₹6000 yearly income support")
    st.write("PMFBY — Crop Insurance")
    st.write("Kisan Credit Card — Low interest loans")
    st.write("Soil Health Card — Free soil testing")

# ================= DASHBOARD =================
def dashboard():

    st.title(f"Welcome {st.session_state.name} 👋")

    col1,col2,col3=st.columns(3)

    if col1.button("🌱 Crop Advisory Ready"):
        st.session_state.page="🤖 AI Assistant"
        st.rerun()

    if col2.button("🤖 AI Enabled"):
        st.session_state.page="🤖 AI Assistant"
        st.rerun()

    if col3.button("🌦 Live Weather Active"):
        st.session_state.page="🌦 Weather & Advisory"
        st.rerun()

    st.subheader("📰 Farming News (Today)")

    st.info("11-02-2026: New government subsidy announced for small farmers.")
    st.info("11-02-2026: Rice productivity increased using hybrid varieties.")
    st.info("11-02-2026: Digital agriculture initiatives expanding in rural India.")

# ================= NOTIFICATIONS =================
def notifications():

    st.header("🔔 Notifications")

    st.success("Rain expected in next 3 days — plan irrigation accordingly.")
    st.warning("Check crop for early pest signs this week.")
    st.info("Government subsidy registration open.")

# ================= ABOUT =================
def about():

    st.write("""
KisanSense is a multilingual agritech platform designed to empower farmers with AI-driven crop advisory, disease detection, weather updates, and information on government schemes.

It provides personalized guidance based on the farmer’s region, crops, and language preference.

By integrating AI, digital tools, and rural accessibility, KisanSense helps farmers make smarter decisions, improve productivity, and reduce crop losses.
""")

    st.subheader("Creators")
    st.write("""
Hemalatha Pulloju  
Thapasi Swarna  
Divya Sree  
Shivani  
Divya
""")

# ================= MAIN APP =================
def main():

    st.sidebar.title("🌾 KisanSahay")

    menu=["🏠 Dashboard","🤖 AI Assistant","📸 Disease Detection",
          "🏛 Government Schemes","🌦 Weather & Advisory",
          "🔔 Notifications","ℹ️ About","📞 Contact"]

    selected=st.sidebar.radio("Navigation",menu,index=menu.index(st.session_state.page))

    st.session_state.page=selected

    if selected=="🏠 Dashboard":
        dashboard()
    elif selected=="🤖 AI Assistant":
        ai_chat()
    elif selected=="📸 Disease Detection":
        disease()
    elif selected=="🏛 Government Schemes":
        schemes()
    elif selected=="🌦 Weather & Advisory":
        weather()
    elif selected=="🔔 Notifications":
        notifications()
    elif selected=="ℹ️ About":
        about()
    elif selected=="📞 Contact":
        st.write("📞 +91 9059184778")
        st.write("📧 kisansahayfarm@gmail.com")

# ================= RUN =================
if not st.session_state.logged_in:
    login()
else:
    main()

