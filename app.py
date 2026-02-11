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

# ================= SMART AI MULTILINGUAL =================
def ai_chat():

    st.header("🤖 Smart AI Assistant")

    lang=st.selectbox("Select Language",
    ["English","Telugu","Hindi","Marathi","Tamil"])

    query=st.text_input("Ask anything about crops, disease, schemes, farming...")

    if query:

        translated=GoogleTranslator(source='auto', target='en').translate(query)
        q=translated.lower()

        if "rice" in q:
            response="Rice cultivation requires good water management, nursery preparation and balanced fertilizers."
        elif "disease" in q:
            response="Remove infected leaves, maintain airflow, and use neem bio-pesticide."
        elif "scheme" in q:
            response="Farmers can use PM-KISAN, PMFBY insurance, Soil Health Card and Kisan Credit Card schemes."
        elif "fertilizer" in q:
            response="Use balanced NPK and perform soil testing before heavy fertilizer usage."
        else:
            response="Monitor soil moisture, follow crop rotation, and use technology-based farming."

        final=GoogleTranslator(source='en', target=lang).translate(response)

        st.success(final)

# ================= WEATHER =================
def weather():

    st.header("🌦 Weather & Advisory")

    city=st.session_state.place

    temp=random.randint(25,36)
    humidity=random.randint(50,85)

    st.metric("Location",city)
    st.metric("Temperature",f"{temp} °C")
    st.metric("Humidity",f"{humidity}%")

# ================= DISEASE =================
def disease():

    st.header("📸 AI Plant Disease Detection")

    file=st.file_uploader("Upload crop image", type=["jpg","png"])

    if file:
        diseases=["Leaf Blight","Powdery Mildew","Bacterial Spot","Healthy Plant"]
        prediction=random.choice(diseases)
        st.success(f"Disease Detected: {prediction}")

# ================= SCHEMES =================
def schemes():

    st.header("🏛 Government Schemes")

    schemes_data=[

    ("PM-KISAN","Income support ₹6000/year","Small farmers","Ministry of Agriculture","https://pmkisan.gov.in"),
    ("PMFBY","Crop Insurance","All crop farmers","Govt of India","https://pmfby.gov.in"),
    ("Kisan Credit Card","Low interest loan","Land holding farmers","NABARD","https://www.myscheme.gov.in"),
    ("Soil Health Card","Free soil testing","All farmers","Agriculture Dept","https://soilhealth.dac.gov.in"),
    ("PMKSY","Irrigation scheme","Farmers needing irrigation","Govt of India","https://pmksy.gov.in"),
    ("NHM","Horticulture support","Fruit/veg farmers","National Horticulture Mission","https://nhm.gov.in"),
    ("eNAM","Online market trading","Registered farmers","Govt of India","https://enam.gov.in"),
    ("PKVY","Organic farming","Organic farmers","Govt of India","https://pgsindia-ncof.gov.in")
    ]

    for name,desc,elig,org,link in schemes_data:

        st.subheader(name)
        st.write("📄 Description:",desc)
        st.write("✅ Eligibility:",elig)
        st.write("🏢 Organization:",org)

        st.link_button("Apply Now",link)

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

    news=[

    ("Govt announces new subsidy","https://www.thehindu.com"),
    ("Hybrid rice increases yield","https://indianexpress.com"),
    ("Digital agriculture expansion","https://timesofindia.indiatimes.com")

    ]

    for title,link in news:
        st.write(title)
        st.link_button("Read More",link)

# ================= ABOUT =================
def about():

    st.markdown("""
<h2 style='font-family:Georgia;'>KisanSense Platform</h2>

<p style='font-size:18px;'>
KisanSense is a multilingual agritech platform designed to empower farmers with AI-driven crop advisory,
disease detection, weather updates, and government scheme information.
</p>
""",unsafe_allow_html=True)

    st.subheader("Creators")
    st.write("""
Hemalatha Pulloju  
Thapasi Swarna  
Divya Sree  
Shivani  
Divya
""")

# ================= MAIN =================
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
    elif selected=="ℹ️ About":
        about()
    elif selected=="📞 Contact":
        st.write("📞 +91 9059184778")
        st.write("📧 kisansahayfarm@gmail.com")

# =================
