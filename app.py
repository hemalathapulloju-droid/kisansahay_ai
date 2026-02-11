import streamlit as st
import requests
from datetime import datetime
from deep_translator import GoogleTranslator

# ================= CONFIG =================

st.set_page_config(page_title="KisanSahay 🌾", layout="wide")

# ================= CSS DESIGN =================

st.markdown("""
<style>
.stApp{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}
.block-container{
background:rgba(0,0,0,0.65);
padding:20px;
border-radius:20px;
}
h1,h2,h3,h4,p,label{color:white !important;}
.stButton>button{
background-color:#2ecc71;
color:white;
border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================

if "login" not in st.session_state:
    st.session_state.login=False

if "applied" not in st.session_state:
    st.session_state.applied=[]

# ================= LOGIN =================

def login_page():
    st.title("🌾 KisanSahay Farmer Login")

    name=st.text_input("Farmer Name")
    place=st.text_input("Village / Location")
    language=st.selectbox("Language",["English","Telugu","Hindi","Marathi"])

    if st.button("Login"):
        st.session_state.login=True
        st.session_state.name=name
        st.session_state.place=place
        st.session_state.lang=language
        st.rerun()

# ================= WEATHER =================

def weather():
    key=st.secrets.get("WEATHER_KEY","")
    if key=="":
        st.warning("Add WEATHER_KEY in secrets")
        return

    city=st.session_state.place
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    res=requests.get(url).json()

    if "main" in res:
        st.metric("Temperature",str(res["main"]["temp"])+" °C")
        st.metric("Humidity",str(res["main"]["humidity"])+"%")
        st.info(res["weather"][0]["description"])

# ================= SMART AI =================

def smart_ai(q):

    # multilingual translate to english internally
    try:
        q=GoogleTranslator(source='auto',target='en').translate(q)
    except:
        pass

    q=q.lower()

    if "rice" in q:
        return "Use nitrogen rich fertilizer during vegetative stage. Maintain standing water."
    elif "scheme" in q:
        return "You can explore PM-Kisan, PMFBY, Soil Health Card scheme in Government Schemes section."
    elif "disease" in q:
        return "Upload image in Disease Detection for AI diagnosis."
    else:
        return "AI Advisory: Monitor soil health, irrigation timing and pest management."

# ================= DISEASE DETECTION =================

def disease_detection():

    st.header("📸 AI Disease Detection")

    img=st.file_uploader("Upload plant image")

    if img:
        st.image(img)

        st.success("Disease detected: Leaf Blight (AI simulated)")
        st.write("### Treatment:")
        st.write("""
        • Remove infected leaves  
        • Spray neem oil  
        • Improve drainage  
        """)

# ================= SCHEMES =================

def schemes():

    st.header("🏛 Government Schemes")

    data=[
        {"name":"PM Kisan","eligibility":"Small farmers","link":"https://pmkisan.gov.in"},
        {"name":"PMFBY Crop Insurance","eligibility":"All farmers","link":"https://pmfby.gov.in"},
        {"name":"Soil Health Card","eligibility":"All farmers","link":"https://soilhealth.dac.gov.in"},
    ]

    for s in data:

        st.subheader(s["name"])
        st.write("Eligibility:",s["eligibility"])

        if st.button("Apply "+s["name"]):
            st.session_state.applied.append(s["name"])
            st.markdown("Apply here 👉 "+s["link"])

    st.divider()

    st.subheader("Application Tracking")

    for a in st.session_state.applied:
        st.success(a+" : In Progress")

# ================= NEWS =================

def news():

    today=datetime.now().strftime("%d-%m-%Y")

    st.header("📰 Farming News")

    st.image("https://images.unsplash.com/photo-1598514982306-7a4cf2f4c43c")

    st.write(today+" : Government announces new subsidy for irrigation.")

    st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef")

    st.write(today+" : AI technology helping Indian farmers increase productivity.")

# ================= DASHBOARD =================

def dashboard():

    st.title("Welcome "+st.session_state.name+" 👋")

    col1,col2,col3=st.columns(3)

    if col1.button("🌱 Crop Advisory"):
        st.session_state.page="AI"

    if col2.button("🤖 AI Assistant"):
        st.session_state.page="AI"

    if col3.button("🌦 Live Weather"):
        st.session_state.page="Weather"

    news()

# ================= MAIN APP =================

def app():

    if "page" not in st.session_state:
        st.session_state.page="Dashboard"

    st.sidebar.title("🌾 KisanSahay")

    nav=st.sidebar.radio("Navigation",[
        "Dashboard",
        "AI Assistant",
        "Disease Detection",
        "Government Schemes",
        "Weather",
        "About",
        "Contact"
    ])

    if nav=="Dashboard":
        dashboard()

    elif nav=="AI Assistant":

        st.title("🤖 Smart AI")

        q=st.text_input("Ask question in any language")

        if st.button("Ask"):
            st.success(smart_ai(q))

        st.file_uploader("🎤 Upload Voice Question")

    elif nav=="Disease Detection":
        disease_detection()

    elif nav=="Government Schemes":
        schemes()

    elif nav=="Weather":
        weather()

    elif nav=="About":

        st.title("About KisanSahay")

        st.write("""
KisanSense is a multilingual agritech platform designed to empower farmers with AI-driven crop advisory,
disease detection, weather updates, and information on government schemes.
It provides personalized guidance based on region and language preference.
""")

        st.subheader("Creators")

        st.write("""
1. Hemalatha Pulloju  
2. Thapasi Swarna  
3. Divya Sree  
4. Shivani  
5. Divya
""")

    elif nav=="Contact":
        st.write("📞 +91 9059184778")
        st.write("📧 kisansahayfarm@gmail.com")

# ================= RUN =================

if not st.session_state.login:
    login_page()
else:
    app()

