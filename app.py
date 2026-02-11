import streamlit as st
import requests
from datetime import datetime

# ====================================
# PAGE CONFIG
# ====================================
st.set_page_config(page_title="KisanSahay", layout="wide")

# ====================================
# CSS DESIGN
# ====================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color:white;
}
.block-container {
    background: rgba(0,0,0,0.6);
    padding:20px;
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

# ====================================
# SESSION
# ====================================
if "logged" not in st.session_state:
    st.session_state.logged = False

if "applied" not in st.session_state:
    st.session_state.applied = []

# ====================================
# LOGIN PAGE
# ====================================
def login():

    st.title("🌾 Welcome to KisanSahay")

    name = st.text_input("Farmer Name")
    place = st.text_input("Village / City")
    language = st.selectbox("Language",
                            ["English","Telugu","Hindi","Marathi","Tamil"])

    if st.button("Login"):
        if name and place:
            st.session_state.logged = True
            st.session_state.user = {
                "name":name,
                "place":place,
                "language":language
            }
            st.rerun()

# ====================================
# SMART AI (NO API)
# ====================================
def smart_ai(q):

    q=q.lower()

    if "rice" in q:
        return "Rice grows best in standing water. Maintain flooded fields, use nitrogen fertilizer and monitor pests."

    elif "aphid" in q or "pest" in q:
        return "Use neem oil spray weekly. Encourage natural predators like ladybird beetles."

    elif "fertilizer" in q:
        return "Use balanced NPK based on soil testing."

    elif "scheme" in q:
        return "Explore PM-KISAN, PMFBY crop insurance and Soil Health Card schemes."

    elif "weather" in q:
        return "Check Weather & Advisory tab for live weather."

    else:
        return "Maintain soil health, monitor irrigation and follow seasonal crop practices."

# ====================================
# WEATHER
# ====================================
def weather(place):

    API_KEY = st.secrets.get("WEATHER_KEY","")

    if not API_KEY:
        st.warning("Add WEATHER_KEY in secrets.")
        return

    url=f"http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}&units=metric"
    data=requests.get(url).json()

    if "main" in data:
        st.metric("Temperature",str(data["main"]["temp"])+" °C")
        st.metric("Humidity",str(data["main"]["humidity"])+" %")
        st.write(data["weather"][0]["description"])

# ====================================
# DISEASE DETECTION (NO API)
# ====================================
def disease():

    st.header("📸 AI Disease Detection")

    file = st.file_uploader("Upload plant leaf image")

    if file:

        # Simulated AI logic (offline)
        filename=file.name.lower()

        if "spot" in filename:
            result="Leaf Spot Disease"
            cure="Remove infected leaves and apply fungicide."
        elif "yellow" in filename:
            result="Yellow Mosaic Virus"
            cure="Control whiteflies and remove infected plants."
        else:
            result="Healthy or unknown disease"
            cure="Monitor regularly and maintain hygiene."

        st.success("Detected: "+result)
        st.write("Treatment:",cure)

# ====================================
# SCHEMES
# ====================================
def schemes():

    st.header("🏛 Government Schemes")

    data=[
        {"name":"PM-KISAN","eligibility":"Small farmers","link":"https://pmkisan.gov.in"},
        {"name":"PMFBY Crop Insurance","eligibility":"All farmers","link":"https://pmfby.gov.in"},
        {"name":"Soil Health Card","eligibility":"All farmers","link":"https://soilhealth.dac.gov.in"},
    ]

    for s in data:
        st.subheader(s["name"])
        st.write("Eligibility:",s["eligibility"])

        if st.button("Apply "+s["name"]):
            st.session_state.applied.append(s["name"])
            st.markdown("[Go to Application Page]("+s["link"]+")")

    st.divider()

    st.subheader("Application Status")

    for a in st.session_state.applied:
        st.write("🟢",a,"- Submitted")

# ====================================
# NEWS
# ====================================
def news():

    st.header("📰 Farming News (India)")
    today=datetime.today().strftime("%d-%m-%Y")

    st.image("https://images.unsplash.com/photo-1598514982306-7a4cf2f4c43c")
    st.write(today,"Government announces new agriculture subsidy support for farmers.")

    st.image("https://images.unsplash.com/photo-1601626200793-15a208f2b8f4")
    st.write(today,"New rice hybrid shows improved yield in Indian climate.")

# ====================================
# DASHBOARD
# ====================================
def dashboard():

    st.title("Welcome "+st.session_state.user["name"])

    col1,col2,col3=st.columns(3)

    if col1.button("🌱 Crop Advisory"):
        st.session_state.page="AI"

    if col2.button("📸 Disease Detection"):
        st.session_state.page="Disease"

    if col3.button("🌦 Weather"):
        st.session_state.page="Weather"

    news()

# ====================================
# MAIN APP
# ====================================
def main():

    st.sidebar.title("🌾 KisanSahay")

    page=st.sidebar.radio("Navigation",[
        "Dashboard",
        "AI Assistant",
        "Disease Detection",
        "Government Schemes",
        "Weather",
        "About",
        "Contact"
    ])

    if page=="Dashboard":
        dashboard()

    elif page=="AI Assistant":

        st.header("🤖 Smart AI")

        q=st.text_input("Ask anything")

        if st.button("Ask"):
            st.success(smart_ai(q))

        st.file_uploader("🎤 Upload Voice Question")

    elif page=="Disease Detection":
        disease()

    elif page=="Government Schemes":
        schemes()

    elif page=="Weather":
        weather(st.session_state.user["place"])

    elif page=="About":

        st.write("""
KisanSense is a multilingual agritech platform designed to empower farmers with AI-driven crop advisory,
disease detection, weather updates and government scheme guidance.

Creators:
1. Hemalatha Pulloju
2. Thapasi Swarna
3. Divya Sree
4. Shivani
5. Divya
""")

    elif page=="Contact":

        st.write("📞 +91 9059184778")
        st.write("📧 kisansahayfarm@gmail.com")

# ====================================
# RUN
# ====================================
if not st.session_state.logged:
    login()
else:
    main()


