import streamlit as st
import requests
from datetime import datetime
from deep_translator import GoogleTranslator

# ================= PAGE CONFIG =================
st.set_page_config(page_title="KisanSahay", layout="wide", page_icon="🌾")

# ================= BACKGROUND =================
st.markdown("""
<style>
.stApp {
background-image: linear-gradient(rgba(0,0,0,0.75),rgba(0,0,0,0.75)),
url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
background-size:cover;
background-attachment:fixed;
color:white;
}
h1,h2,h3,h4,p,label {color:white;}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "login" not in st.session_state:
    st.session_state.login=False
if "applied" not in st.session_state:
    st.session_state.applied=[]

# ================= LOGIN PAGE =================
def login():
    st.title("🌾 KisanSahay Farmer Login")

    name = st.text_input("Farmer Name")
    place = st.text_input("Village / City")
    language = st.selectbox("Language",
                            ["English","Telugu","Hindi","Marathi","Tamil"])

    if st.button("Login"):
        if name:
            st.session_state.login=True
            st.session_state.name=name
            st.session_state.place=place
            st.session_state.language=language
            st.rerun()

# ================= SMART AI =================
def smart_ai(query):

    # multilingual translate
    try:
        query = GoogleTranslator(source='auto', target='en').translate(query)
    except:
        pass

    q = query.lower()

    if "rice" in q:
        return "Rice growing: Prepare nursery, maintain water level 2-5cm, use balanced NPK fertilizer."
    elif "aphid" in q:
        return "Use neem oil spray and encourage natural predators."
    elif "scheme" in q:
        return "Check Government Schemes tab for PM-Kisan, PMFBY, Soil Health Card."
    elif "weather" in q:
        return "Open Weather Advisory section."
    else:
        return "AI Advisory: Maintain soil health, monitor pests, use certified seeds and irrigation management."

# ================= WEATHER =================
def weather():
    st.header("🌦 Weather Advisory")

    key = st.secrets.get("WEATHER_KEY","")

    if key=="":
        st.warning("Add WEATHER_KEY in secrets.")
        return

    city = st.session_state.place

    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    data=requests.get(url).json()

    if "main" in data:
        st.success(f"Temperature: {data['main']['temp']}°C")
        st.info(data['weather'][0]['description'])
    else:
        st.error("Weather not found.")

# ================= DISEASE DETECTION =================
def disease():
    st.header("📸 AI Plant Disease Detection")

    file = st.file_uploader("Upload plant image")

    if file:
        hf = st.secrets.get("HF_API_KEY","")

        if hf=="":
            st.warning("Add HF_API_KEY in secrets.")
            return

        API="https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
        headers={"Authorization":f"Bearer {hf}"}

        response=requests.post(API,headers=headers,data=file.read())

        try:
            result=response.json()[0]["label"]
            st.success(f"Disease detected: {result}")
            st.write("Treatment:")
            st.write("- Remove infected leaves")
            st.write("- Neem oil spray")
        except:
            st.error("Could not detect disease.")

# ================= GOVERNMENT SCHEMES =================
def schemes():

    st.header("🏛 Government Schemes")

    data=[
        ("PM-Kisan","All farmers","₹6000/year","https://pmkisan.gov.in"),
        ("PMFBY","Crop growers","Crop insurance","https://pmfby.gov.in"),
        ("Soil Health Card","All farmers","Free soil testing","https://soilhealth.dac.gov.in")
    ]

    for name,elig,benefit,link in data:
        st.subheader(name)
        st.write("Eligibility:",elig)
        st.write("Benefit:",benefit)

        if st.button(f"Apply {name}"):
            st.session_state.applied.append(name)
            st.markdown(f"[Apply on Official Website]({link})")

    st.divider()

    st.subheader("Application Tracking")

    if st.session_state.applied:
        for s in st.session_state.applied:
            st.success(f"{s} — Application Submitted")
    else:
        st.info("No schemes applied yet.")

# ================= NEWS =================
def news():

    st.header("📰 Agriculture News India")

    today=datetime.today().strftime("%d-%m-%Y")

    st.subheader("Government launches new subsidy scheme")
    st.write(today)
    st.image("https://images.unsplash.com/photo-1598514982306-7a4cf2f4c43c",width=400)
    st.write("New policies aim to support farmers through technology and subsidies.")

# ================= DASHBOARD =================
def dashboard():

    st.title(f"Welcome {st.session_state.name}")

    col1,col2,col3=st.columns(3)

    with col1:
        if st.button("🌱 Crop Advisory"):
            st.session_state.page="AI"

    with col2:
        if st.button("🌦 Live Weather Active"):
            st.session_state.page="Weather"

    with col3:
        if st.button("🤖 AI Assistant"):
            st.session_state.page="AI"

    news()

# ================= MAIN APP =================
def main():

    if "page" not in st.session_state:
        st.session_state.page="Dashboard"

    st.sidebar.title("🌾 KisanSahay")

    page=st.sidebar.radio("Navigation",
    ["🏠 Dashboard","🤖 AI Assistant","📸 Disease Detection","🏛 Government Schemes","🌦 Weather & Advisory","ℹ️ About","📞 Contact"])

    if page=="🏠 Dashboard":
        dashboard()

    elif page=="🤖 AI Assistant":
        st.header("🤖 Smart AI")

        q=st.text_input("Ask any farming question (Any language)")
        if q:
            st.success(smart_ai(q))

    elif page=="📸 Disease Detection":
        disease()

    elif page=="🏛 Government Schemes":
        schemes()

    elif page=="🌦 Weather & Advisory":
        weather()

    elif page=="ℹ️ About":
        st.write("""
KisanSense is a multilingual agritech platform designed to empower farmers with AI-driven crop advisory, disease detection, weather updates, and government scheme information.

Creators:
1. Hemalatha Pulloju
2. Thapasi Swarna
3. Divya Sree
4. Shivani
5. Divya
""")

    elif page=="📞 Contact":
        st.write("📞 +91 9059184778")
        st.write("📧 kisansahayfarm@gmail.com")

# ================= RUN =================
if not st.session_state.login:
    login()
else:
    main()
