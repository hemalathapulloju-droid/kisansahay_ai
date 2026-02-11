import streamlit as st
import requests
from datetime import datetime
from deep_translator import GoogleTranslator
from PIL import Image

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="KisanSahay",
    layout="wide",
    page_icon="🌾"
)

# ================= BACKGROUND & CSS =================
st.markdown("""
<style>
.stApp{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}
h1,h2,h3,h4,h5,h6,p,label{color:white !important;}
.stButton>button{background-color:#2ecc71;color:white;border-radius:10px;height:3em;width:100%;font-size:16px;}
.block-container{background: rgba(0,0,0,0.65); padding:20px; border-radius:20px;}
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "chat" not in st.session_state:
    st.session_state.chat = []

if "applied_schemes" not in st.session_state:
    st.session_state.applied_schemes = []

# ================= LOGIN PAGE =================
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
            st.session_state.farmer = {"name": name, "place": place, "land": land, "phone": phone, "language": language}
            st.rerun()
        else:
            st.warning("Please fill required details")

# ================= SMART AI =================
def smart_ai(query):
    q = query.lower()
    if "fertilizer" in q:
        return "Use soil testing before fertilizer. Apply balanced NPK. Avoid overuse."
    elif "disease" in q:
        return "Use crop image upload in Disease Detection to get AI diagnosis."
    elif "scheme" in q:
        return "Explore PM-Kisan, PMFBY, Soil Health Card, KCC, and other govt schemes."
    elif "weather" in q:
        return "Check Weather & Advisory tab for real-time updates based on your location."
    else:
        return "AI Advisory: Monitor crops, follow seasonal patterns, adopt modern techniques, and consult local officers."

# ================= WEATHER =================
def get_weather(place):
    API_KEY = st.secrets.get("WEATHER_KEY","")
    if not API_KEY:
        st.warning("Add WEATHER_KEY in secrets to get weather info")
        return
    url = f"http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}&units=metric"
    res = requests.get(url).json()
    if res.get("main"):
        temp = res["main"]["temp"]
        humidity = res["main"]["humidity"]
        desc = res["weather"][0]["description"]
        st.metric("Temperature", f"{temp}°C")
        st.metric("Humidity", f"{humidity}%")
        st.info(desc)
    else:
        st.error("Weather not found for your location.")

# ================= DISEASE DETECTION =================
def disease_detection():
    st.header("📸 AI Plant Disease Detection")
    file = st.file_uploader("Upload Leaf Image", type=["jpg","png"])
    if file:
        HF_KEY = st.secrets.get("HF_API_KEY","")
        if not HF_KEY:
            st.warning("Add HF_API_KEY in secrets to detect disease")
            return
        API_URL = "https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
        headers = {"Authorization": f"Bearer {HF_KEY}"}
        res = requests.post(API_URL, headers=headers, data=file.read())
        try:
            prediction = res.json()[0]["label"]
            st.success(f"Disease Detected: {prediction}")
            st.write("### Recommended Actions")
            st.write("- Remove infected leaves")
            st.write("- Apply neem oil / bio-pesticide")
            st.write("- Maintain proper spacing and airflow")
        except:
            st.error("Could not detect disease, please try clearer image.")

# ================= GOVERNMENT SCHEMES =================
def show_schemes():
    st.header("🏛 Government Schemes")
    schemes = [
        {"name":"PM-KISAN","eligibility":"All small & marginal farmers","benefit":"₹6000/year","link":"https://pmkisan.gov.in/"},
        {"name":"PMFBY Crop Insurance","eligibility":"Farmers growing notified crops","benefit":"Insurance against crop loss","link":"https://pmfby.gov.in/"},
        {"name":"Kisan Credit Card","eligibility":"Farmers with land","benefit":"Low-interest loans","link":"https://www.myscheme.gov.in/schemes/kcc"},
        {"name":"Soil Health Card","eligibility":"All farmers","benefit":"Free soil testing","link":"https://soilhealth.dac.gov.in/"}
    ]
    for s in schemes:
        st.subheader(s["name"])
        st.write(f"✅ Eligibility: {s['eligibility']}")
        st.write(f"💰 Benefit: {s['benefit']}")
        if st.button(f"Apply for {s['name']}"):
            st.session_state.applied_schemes.append(s["name"])
            st.success("Redirecting to official application page...")
            st.markdown(f"[Apply Here]({s['link']})")

    st.divider()
    st.subheader("📊 Applied Schemes Tracking")
    if st.session_state.applied_schemes:
        for a in st.session_state.applied_schemes:
            st.write(f"🟢 {a} — In Progress")
    else:
        st.info("No schemes applied yet.")

# ================= NEWS =================
def show_news():
    st.header("📰 Latest Agriculture News")
    today = datetime.today().strftime("%d-%m-%Y")
    news_items = [
        {"title":"Government launches new crop subsidy","desc":"PM-KISAN 2.0 launched for all farmers","img":"https://images.unsplash.com/photo-1601626200793-15a208f2b8f4"},
        {"title":"Rice yield increases","desc":"New hybrid varieties show 10% yield increase","img":"https://images.unsplash.com/photo-1598514982306-7a4cf2f4c43c"}
    ]
    for n in news_items:
        st.subheader(n["title"])
        st.image(n["img"], width=400)
        st.write(f"{today}: {n['desc']}")

# ================= DASHBOARD =================
def dashboard():
    st.title(f"Welcome {st.session_state.farmer['name']} 👋")
    col1,col2,col3 = st.columns(3)
    if col1.button("🌱 Crop Advisory"):
        st.experimental_rerun()
    if col2.button("🤖 AI Assistant"):
        st.experimental_rerun()
    if col3.button("🌦 Weather"):
        st.experimental_rerun()
    show_news()
    st.info("Live advisory, AI, and weather modules available from sidebar navigation.")

# ================= SIDEBAR =================
def main_app():
    st.sidebar.title("🌾 KisanSahay")
    menu = st.sidebar.radio("Navigation", [
        "🏠 Dashboard",
        "🤖 AI Assistant",
        "📸 Disease Detection",
        "🏛 Government Schemes",
        "🌦 Weather & Advisory",
        "🔔 Notifications",
        "ℹ️ About",
        "📞 Contact"
    ])
    st.sidebar.write(f"👤 {st.session_state.farmer['name']}")
    st.sidebar.write(f"📍 {st.session_state.farmer['place']}")
    st.sidebar.write(f"🌾 {st.session_state.farmer['land']}")

    if menu=="🏠 Dashboard":
        dashboard()
    elif menu=="🤖 AI Assistant":
        st.title("🤖 Smart AI Assistant")
        ai_chat = st.text_area("Ask your question in any language:")
        if st.button("Ask AI"):
            if ai_chat:
                answer = smart_ai(ai_chat)
                st.success(answer)
    elif menu=="📸 Disease Detection":
        disease_detection()
    elif menu=="🏛 Government Schemes":
        show_schemes()
    elif menu=="🌦 Weather & Advisory":
        get_weather(st.session_state.farmer["place"])
    elif menu=="🔔 Notifications":
        st.title("🔔 Notifications")
        st.info("No new alerts today")
    elif menu=="ℹ️ About":
        st.title("About KisanSahay")
        st.write("""
KisanSahay is a multilingual agritech platform designed to empower farmers with AI-driven crop advisory, disease detection, weather updates, and information on government schemes.
It provides personalized guidance based on the farmer’s region, crops, and language preference. By integrating AI, digital tools, and rural accessibility, KisanSahay helps farmers make smarter decisions, improve productivity, and reduce crop losses.
""")
        st.subheader("Creators")
        st.write("1. Hemalatha Pulloju\n2. Thapasi Swarna\n3. Divya Sree\n4. Shivani\n5. Divya")
    elif menu=="📞 Contact":
        st.title("Contact")
        st.write("📞 +91 9059184778")
        st.write("📧 kisansahayfarm@gmail.com")
        msg = st.text_area("Send us a message:")
        if st.button("Submit"):
            st.success("Thank you! We will contact you shortly.")

# ================= RUN =================
if not st.session_state.logged_in:
    login()
else:
    main_app()




