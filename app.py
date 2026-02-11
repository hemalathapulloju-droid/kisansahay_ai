import streamlit as st
import requests
from datetime import datetime
from deep_translator import GoogleTranslator

# ================= PAGE CONFIG =================
st.set_page_config(page_title="KisanSahay", layout="wide")

# ================= BACKGROUND =================
st.markdown("""
<style>
.stApp {
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}
h1,h2,h3,h4,h5,p,label{
color:white !important;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "chat" not in st.session_state:
    st.session_state.chat = []

# ================= LOGIN =================
def login():
    st.title("🌾 KisanSahay Farmer Login")

    name = st.text_input("Farmer Name")
    place = st.text_input("Village / City")
    language = st.selectbox("Language",["English","Telugu","Hindi","Marathi","Tamil"])

    if st.button("Login"):
        if name and place:
            st.session_state.logged_in = True
            st.session_state.name = name
            st.session_state.place = place
            st.session_state.language = language
            st.rerun()

# ================= SMART AI =================
def smart_ai(q):

    translated = GoogleTranslator(source='auto',target='en').translate(q)
    query = translated.lower()

    if "rice" in query:
        ans = "For rice cultivation: prepare nursery, maintain water level, use nitrogen fertilizer, and monitor pests."
    elif "scheme" in query:
        ans = "Major schemes include PM-Kisan, PMFBY, Soil Health Card, KCC."
    elif "disease" in query:
        ans = "Upload plant image in disease detection section for AI diagnosis."
    else:
        ans = "Follow seasonal practices, soil testing, balanced fertilizer use and crop monitoring."

    final = GoogleTranslator(source='en',target='auto').translate(ans)
    return final

# ================= WEATHER =================
def weather():

    st.header("🌦 Weather Advisory")

    key = st.secrets.get("WEATHER_KEY","")

    if not key:
        st.warning("Add WEATHER_KEY in secrets for real weather.")
        return

    city = st.session_state.place

    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    data=requests.get(url).json()

    if "main" in data:
        st.metric("Temperature",f"{data['main']['temp']} °C")
        st.metric("Humidity",f"{data['main']['humidity']} %")
        st.info(data['weather'][0]['description'])

# ================= NEWS =================
def news():

    st.header("📰 Agriculture News (India)")

    today = datetime.today().strftime("%d-%m-%Y")
    st.write("Date:",today)

    st.image("https://images.unsplash.com/photo-1598514982306-7a4cf2f4c43c",width=400)
    st.write("Government announces new fertilizer subsidy policy for farmers.")

    st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef",width=400)
    st.write("New AI-based agriculture technologies introduced across India.")

# ================= SCHEMES =================
def schemes():

    st.header("🏛 Government Schemes")

    schemes_data = [
        ("PM-KISAN","Small farmers","₹6000/year","https://pmkisan.gov.in/"),
        ("PMFBY Crop Insurance","All crop farmers","Insurance coverage","https://pmfby.gov.in/"),
        ("Soil Health Card","All farmers","Free soil testing","https://soilhealth.dac.gov.in/")
    ]

    for s in schemes_data:
        st.subheader(s[0])
        st.write("Eligibility:",s[1])
        st.write("Benefit:",s[2])
        st.markdown(f"[Apply Here]({s[3]})")

# ================= DISEASE =================
def disease():

    st.header("📸 AI Disease Detection")

    file = st.file_uploader("Upload plant image")

    if file:
        st.success("Image received. (AI prediction placeholder ready for API integration)")
        st.write("Possible Disease: Leaf Spot")
        st.write("Treatment: Neem oil spray, remove infected leaves.")

# ================= AI CHAT =================
def chatbot():

    st.header("🤖 Smart AI Assistant")

    q = st.text_input("Ask farming question (any language)")

    audio = st.file_uploader("🎤 Upload Voice Question",type=["wav","mp3"])

    if audio:
        st.info("Voice received (speech-to-text can be added later).")

    if q:
        ans = smart_ai(q)
        st.success(ans)

# ================= DASHBOARD =================
def dashboard():

    st.title(f"Welcome {st.session_state.name} 👋")

    col1,col2,col3 = st.columns(3)

    if col1.button("🌱 Crop Advisory"):
        st.session_state.page="🤖 AI Assistant"

    if col2.button("🤖 AI Enabled"):
        st.session_state.page="🤖 AI Assistant"

    if col3.button("🌦 Live Weather"):
        st.session_state.page="🌦 Weather & Advisory"

    news()

# ================= MAIN APP =================
def main():

    if "page" not in st.session_state:
        st.session_state.page="🏠 Dashboard"

    page = st.sidebar.radio("Navigation",
    ["🏠 Dashboard","🤖 AI Assistant","📸 Disease Detection","🏛 Government Schemes","🌦 Weather & Advisory","ℹ️ About","📞 Contact"])

    if page=="🏠 Dashboard":
        dashboard()

    elif page=="🤖 AI Assistant":
        chatbot()

    elif page=="📸 Disease Detection":
        disease()

    elif page=="🏛 Government Schemes":
        schemes()

    elif page=="🌦 Weather & Advisory":
        weather()

    elif page=="ℹ️ About":

        st.write("""
KisanSense is a multilingual agritech platform designed to empower farmers with AI-driven crop advisory, disease detection, weather updates, and information on government schemes.

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
if not st.session_state.logged_in:
    login()
else:
    main()


