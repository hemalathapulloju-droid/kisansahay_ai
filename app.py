import streamlit as st
import requests
from datetime import datetime
from deep_translator import GoogleTranslator
from PIL import Image

# ================= PAGE CONFIG =================
st.set_page_config(page_title="KisanSahay", layout="wide", page_icon="🌾")

# ================= PREMIUM UI =================
st.markdown("""
<style>
.stApp{
background: linear-gradient(rgba(0,0,0,0.7),rgba(0,0,0,0.8)),
url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
background-size:cover;
color:white;
}
.block-container{
background:rgba(0,0,0,0.65);
padding:20px;
border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "login" not in st.session_state:
    st.session_state.login=False

if "applied" not in st.session_state:
    st.session_state.applied=[]

# ================= LOGIN PAGE =================
def login():

    st.title("🌾 KisanSahay")

    name=st.text_input("Farmer Name")
    place=st.text_input("Village / Location")
    lang=st.selectbox("Language",["English","Telugu","Hindi","Marathi"])

    if st.button("LOGIN"):
        if name and place:
            st.session_state.login=True
            st.session_state.name=name
            st.session_state.place=place
            st.session_state.lang=lang
            st.rerun()

# ================= SMART AI =================
def smart_ai(q):

    q=q.lower()

    if "rice" in q:
        return "Rice grows best in warm climate. Maintain standing water and apply balanced fertilizer."

    if "scheme" in q:
        return "You can check PM-KISAN, PMFBY, Soil Health Card schemes in Government Schemes section."

    if "disease" in q:
        return "Upload leaf image in Disease Detection tab for AI diagnosis."

    return "AI Advisory: Monitor soil health, use certified seeds, follow seasonal practices."

# ================= WEATHER =================
def weather():

    key=st.secrets.get("WEATHER_KEY","")

    if not key:
        st.warning("Add WEATHER_KEY in secrets.")
        return

    city=st.session_state.place

    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"

    res=requests.get(url).json()

    if "main" in res:
        st.metric("Temperature",str(res["main"]["temp"])+" °C")
        st.metric("Humidity",str(res["main"]["humidity"])+"%")
        st.info(res["weather"][0]["description"])
    else:
        st.error("Weather unavailable.")

# ================= DISEASE DETECTION =================
def disease():

    st.header("📸 AI Disease Detection")

    file=st.file_uploader("Upload plant image")

    if file:

        HF=st.secrets.get("HF_API_KEY","")

        if not HF:
            st.error("Add HF_API_KEY in secrets")
            return

        API="https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"

        headers={"Authorization":f"Bearer {HF}"}

        res=requests.post(API,headers=headers,data=file.read())

        try:
            result=res.json()[0]["label"]
            st.success("Disease Detected: "+result)
            st.write("Recommended:")
            st.write("• Remove infected leaves")
            st.write("• Apply neem oil spray")
        except:
            st.error("Detection failed")

# ================= SCHEMES =================
def schemes():

    st.header("🏛 Government Schemes")

    data=[

        {"name":"PM-KISAN",
         "eligibility":"All small farmers",
         "benefit":"₹6000 yearly",
         "link":"https://pmkisan.gov.in/"},

        {"name":"PMFBY Crop Insurance",
         "eligibility":"Crop growers",
         "benefit":"Insurance protection",
         "link":"https://pmfby.gov.in/"},

        {"name":"Soil Health Card",
         "eligibility":"All farmers",
         "benefit":"Free soil testing",
         "link":"https://soilhealth.dac.gov.in/"}

    ]

    for s in data:

        st.subheader(s["name"])
        st.write("Eligibility:",s["eligibility"])
        st.write("Benefit:",s["benefit"])

        if st.button("Apply "+s["name"]):
            st.session_state.applied.append(s["name"])
            st.success("Apply here:")
            st.markdown(s["link"])

    st.divider()

    st.subheader("📊 Application Status")

    for a in st.session_state.applied:
        st.write("🟢",a,"In Progress")

# ================= NEWS =================
def news():

    st.header("📰 Agriculture News")

    today=datetime.now().strftime("%d-%m-%Y")

    st.image("https://images.unsplash.com/photo-1598514982306-7a4cf2f4c43c",width=400)

    st.write(today,"Government announces new fertilizer subsidy policy.")

    st.image("https://images.unsplash.com/photo-1601626200793-15a208f2b8f4",width=400)

    st.write(today,"Rice yield improves with hybrid seeds.")

# ================= DASHBOARD =================
def dashboard():

    st.title("Welcome "+st.session_state.name)

    col1,col2,col3=st.columns(3)

    if col1.button("🌱 Crop Advisory"):
        st.session_state.page="AI"

    if col2.button("🤖 AI Assistant"):
        st.session_state.page="AI"

    if col3.button("🌦 Weather"):
        st.session_state.page="Weather"

    news()

# ================= MAIN APP =================
def main():

    st.sidebar.title("🌾 KisanSahay")

    menu=st.sidebar.radio("Navigation",[

        "🏠 Dashboard",
        "🤖 AI Assistant",
        "📸 Disease Detection",
        "🏛 Government Schemes",
        "🌦 Weather & Advisory",
        "ℹ️ About",
        "📞 Contact"

    ])

    if menu=="🏠 Dashboard":
        dashboard()

    if menu=="🤖 AI Assistant":

        st.header("🤖 Smart AI")

        q=st.text_area("Ask anything (English / Telugu / Hindi etc)")

        if st.button("Ask"):
            ans=smart_ai(q)

            lang=st.session_state.lang

            if lang!="English":
                ans=GoogleTranslator(source='auto',target=lang.lower()).translate(ans)

            st.success(ans)

    if menu=="📸 Disease Detection":
        disease()

    if menu=="🏛 Government Schemes":
        schemes()

    if menu=="🌦 Weather & Advisory":
        weather()

    if menu=="ℹ️ About":

        st.write("""
KisanSense is a multilingual agritech platform designed to empower farmers with AI-driven crop advisory, disease detection, weather updates, and information on government schemes.

Creators:
1. Hemalatha Pulloju
2. Thapasi Swarna
3. Divya Sree
4. Shivani
5. Divya
""")

    if menu=="📞 Contact":

        st.write("📞 +91 9059184778")
        st.write("📧 kisansahayfarm@gmail.com")

# ================= RUN =================

if not st.session_state.login:
    login()
else:
    main()
        st.write("📧 kisansahayfarm@gmail.com")

# =================

