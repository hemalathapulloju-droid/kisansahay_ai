import streamlit as st
import random
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="KisanSahay", layout="wide", page_icon="🌾")

# =====================================================
# BACKGROUND UI
# =====================================================
st.markdown("""
<style>
.stApp{
background-image: linear-gradient(rgba(0,0,0,0.75),rgba(0,0,0,0.75)),
url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
background-size: cover;
}
h1,h2,h3,h4,h5,p,label{color:white !important;}
.stButton>button{
background:#2ecc71;
color:white;
border-radius:12px;
}
.block-container{
background: rgba(0,0,0,0.65);
padding:20px;
border-radius:20px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in=False

if "page" not in st.session_state:
    st.session_state.page="🏠 Dashboard"

# =====================================================
# OFFLINE LANGUAGE PREFIX (NO API)
# =====================================================
def translate_text(text, lang):

    prefix = {
        "Telugu": "🌾 వ్యవసాయ సూచన: ",
        "Hindi": "🌾 कृषि सलाह: ",
        "Tamil": "🌾 வேளாண்மை ஆலோசனை: ",
        "Marathi": "🌾 शेती सल्ला: ",
        "Kannada": "🌾 ಕೃಷಿ ಸಲಹೆ: ",
        "English": ""
    }

    return prefix.get(lang,"") + text

# =====================================================
# LOGIN PAGE
# =====================================================
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
        ["English","Telugu","Hindi","Marathi","Tamil","Kannada"])

    if st.button("Login"):
        if name and place:
            st.session_state.logged_in=True
            st.session_state.name=name
            st.session_state.place=place
            st.session_state.land=land
            st.session_state.language=language
            st.rerun()

# =====================================================
# SMART AI ASSISTANT (NO API + BIG ANSWERS + PREDICTION)
# =====================================================
def ai_chat():

    st.header("🤖 Smart AI Assistant")

    lang=st.selectbox("Select Answer Language",
    ["English","Telugu","Hindi","Marathi","Tamil","Kannada"])

    query=st.text_area("Ask anything about farming, crops, fertilizer, schemes, weather...")

    if st.button("Submit Question"):

        if query:

            q=query.lower()

            knowledge_base={

            "rice":"""Rice cultivation requires proper water management, good nursery preparation, and correct transplantation timing. Farmers should maintain standing water during early growth stages and gradually reduce water before harvesting. Using balanced nitrogen fertilizer improves leaf growth and grain quality. Farmers must also monitor pests like stem borer and leaf folder regularly. Proper spacing and weed management significantly increase yield.""",

            "fertilizer":"""Fertilizers are essential for crop productivity. Farmers must use balanced NPK fertilizers based on soil test results. Excess nitrogen can cause pest attacks and weak stems. Organic fertilizers like compost improve soil microbial activity and long-term fertility. Split fertilizer application ensures better nutrient absorption and reduces wastage. Farmers should also consider micronutrients like zinc and boron for better crop development.""",

            "scheme":"""Government schemes support farmers financially and technically. PM-KISAN provides direct income support to farmers. PMFBY crop insurance protects against crop loss due to natural disasters. Soil Health Card helps farmers understand soil nutrient levels and fertilizer recommendations. Kisan Credit Card provides low-interest loans. Farmers should regularly check official portals and local agriculture offices for new scheme updates and subsidy opportunities.""",

            "weather":"""Weather plays a major role in farming success. Farmers must plan irrigation based on rainfall forecast and temperature trends. During high temperature periods, mulching helps retain soil moisture. During heavy rainfall periods, proper drainage prevents root rot. Humidity increase can trigger fungal diseases, so preventive spraying is important. Weather-based farming planning helps increase productivity and reduce risk.""",

            "disease":"""Plant diseases spread due to fungus, bacteria, or viruses. Farmers must monitor leaves regularly for spots, discoloration, or unusual patterns. Early detection helps prevent full crop damage. Neem oil and bio pesticides are safe preventive solutions. Removing infected plant parts prevents spread. Maintaining field hygiene and proper spacing reduces disease risk significantly."""
            }

            response="Smart farming requires soil health monitoring, balanced fertilizer use, pest monitoring, and climate-based decision making."

            for key in knowledge_base:
                if key in q:
                    response=knowledge_base[key]

            # Prediction style add-on
            prediction_add = """

📊 Future Farming Prediction:
• Yield can increase by 15-25% if balanced fertilizer and irrigation used.
• Pest risk may increase during humidity rise.
• Climate smart farming improves profit stability.
• Soil organic matter improvement increases long term productivity.
"""

            final_text = translate_text(response + prediction_add, lang)

            st.success(final_text)

# =====================================================
# DISEASE DETECTION (SIMULATION)
# =====================================================
def disease():

    st.header("📸 AI Plant Disease Detection")

    file=st.file_uploader("Upload leaf image", type=["jpg","png"])

    if file:

        diseases=[
        ("Leaf Blight","Fungal infection causing brown patches."),
        ("Powdery Mildew","White powder on leaf surface."),
        ("Bacterial Spot","Yellow lesions spreading rapidly."),
        ("Healthy Plant","No disease detected.")
        ]

        pred=random.choice(diseases)

        st.success(f"Disease: {pred[0]}")

        st.write(f"""
Detailed Analysis Report:

{pred[1]}

Prevention & Control:
• Remove infected leaves
• Use neem pesticide
• Maintain spacing
• Avoid over irrigation
• Monitor crop daily
""")

# =====================================================
# WEATHER WITH DATE
# =====================================================
def weather():

    st.header("🌦 Weather & Advisory")

    today=datetime.now()

    st.write(f"📍 Location: {st.session_state.place}")
    st.write(f"📅 Date: {today.strftime('%d %B %Y')}")

    cols=st.columns(4)

    cols[0].metric("Temperature",f"{random.randint(25,34)}°C")
    cols[1].metric("Humidity",f"{random.randint(50,90)}%")
    cols[2].metric("Rain Chance",f"{random.randint(10,80)}%")
    cols[3].metric("Wind Speed",f"{random.randint(5,25)} km/h")

    st.info("Apply fertilizer during cool hours.")
    st.warning("Monitor pests during humidity increase.")

# =====================================================
# DASHBOARD WITH NEWSPAPER STYLE NEWS
# =====================================================
def dashboard():

    st.title(f"Welcome {st.session_state.name} 👋")

    st.subheader("📰 Agriculture Current Affairs — Newspaper Style")

    st.write("""
India is rapidly moving towards digital agriculture and climate smart farming practices. Government and private sectors are investing heavily in precision farming, AI crop monitoring, and smart irrigation systems. Recently, new subsidy programs were introduced to support small and marginal farmers in purchasing modern farming equipment. Hybrid crop varieties are showing higher productivity and better climate resistance. Experts suggest farmers adopt soil testing, crop rotation, and organic matter enrichment to improve long term sustainability. Digital advisory platforms are helping farmers make real-time decisions based on weather, market price, and pest alerts. These developments are expected to improve farmer income and reduce crop failure risks across India.
""")

# =====================================================
# MAIN NAVIGATION
# =====================================================
def main():

    st.sidebar.title("🌾 KisanSahay")

    menu=["🏠 Dashboard","🤖 AI Assistant","📸 Disease Detection","🌦 Weather & Advisory"]

    selected=st.sidebar.radio("Navigation",menu)

    if selected=="🏠 Dashboard":
        dashboard()
    elif selected=="🤖 AI Assistant":
        ai_chat()
    elif selected=="📸 Disease Detection":
        disease()
    elif selected=="🌦 Weather & Advisory":
        weather()

# =====================================================
# RUN
# =====================================================
if not st.session_state.logged_in:
    login()
else:
    main()


