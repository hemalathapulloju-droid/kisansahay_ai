import streamlit as st
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="KisanSahay",
    page_icon="🌾",
    layout="wide"
)

# =====================================================
# DARK PROFESSIONAL UI (Fixes White Background Issue)
# =====================================================
st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

[data-testid="stSidebar"]{
background: linear-gradient(180deg,#1c1c1c,#2b5876);
}

h1,h2,h3,h4{
color:#E8F6EF;
}

.stButton>button{
background-color:#00c853;
color:white;
border-radius:10px;
height:3em;
width:100%;
font-size:16px;
}

.stTextInput>div>div>input{
background-color:#2b2b2b;
color:white;
}

.stSelectbox>div{
background-color:#2b2b2b;
}

.card{
padding:20px;
border-radius:15px;
background: rgba(255,255,255,0.05);
box-shadow:0 8px 32px rgba(0,0,0,0.37);
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
if "chat" not in st.session_state:
    st.session_state.chat = []

if "farmer" not in st.session_state:
    st.session_state.farmer = {
        "name":"Hema Farmer",
        "village":"Warangal",
        "land":"<1 Acre"
    }

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("🌾 KisanSahay")

page = st.sidebar.radio("Navigation",[
"🏠 Dashboard",
"🤖 AI Assistant",
"🌱 Crop Recommendation",
"📸 Disease Detection",
"🏛 Government Schemes",
"🌦 Weather & Advisory",
"🔔 Notifications",
"ℹ️ About",
"📞 Contact"
])

st.sidebar.markdown("---")
st.sidebar.write("👩‍🌾 **Farmer Profile**")
st.sidebar.write(f"Name: {st.session_state.farmer['name']}")
st.sidebar.write(f"Village: {st.session_state.farmer['village']}")
st.sidebar.write(f"Land: {st.session_state.farmer['land']}")

# =====================================================
# AI BRAIN (Answers Almost Anything Agriculture)
# =====================================================
def smart_agri_ai(q):

    q = q.lower()

    data = {

        "fertilizer":
        """✅ Use soil testing before fertilizer.
        
• Nitrogen → Leaf growth  
• Phosphorus → Root strength  
• Potassium → Disease resistance  

Avoid overuse!""",

        "pest":
        """🐛 Integrated Pest Management:

• Neem oil spray  
• Crop rotation  
• Biological predators  
• Minimal chemical usage""",

        "water":
        """💧 Irrigation Tips:

• Early morning watering  
• Drip irrigation saves 60% water  
• Avoid waterlogging""",

        "profit":
        """💰 Increase Farm Profit:

• Choose high-demand crops  
• Use government subsidies  
• Sell directly via FPO / markets  
• Reduce chemical dependency"""
    }

    for key in data:
        if key in q:
            return data[key]

    return """
🌾 Smart Advisory:

• Follow seasonal crop patterns  
• Monitor weather regularly  
• Use certified seeds  
• Adopt AI & modern farming  

👉 For best results consult local agriculture officer.
"""

# =====================================================
# DASHBOARD
# =====================================================
if page=="🏠 Dashboard":

    st.title("🚜 Welcome to KisanSahay")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">🌱 Crop AI<br><br>Get intelligent crop predictions.</div>',unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">🤖 Smart Farming Assistant<br><br>Ask anything about agriculture.</div>',unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">🏛 Govt Schemes<br><br>Unlock subsidies & benefits.</div>',unsafe_allow_html=True)

    st.markdown("### 📊 Today's Insight")

    st.success("✅ Weather looks favorable for irrigation.")

# =====================================================
# AI CHATBOT
# =====================================================
elif page=="🤖 AI Assistant":

    st.title("🤖 Kisan AI Expert")

    user = st.chat_input("Ask ANY farming question...")

    if user:
        st.session_state.chat.append(("You",user))
        reply = smart_agri_ai(user)
        st.session_state.chat.append(("AI",reply))

    for sender,msg in st.session_state.chat:
        st.chat_message(sender).write(msg)

# =====================================================
# CROP RECOMMENDATION
# =====================================================
elif page=="🌱 Crop Recommendation":

    st.title("🌱 AI Crop Predictor")

    soil = st.selectbox("Soil Type",["Black","Red","Sandy","Clay"])
    season = st.selectbox("Season",["Kharif","Rabi","Zaid"])

    if st.button("Predict Crops"):

        crops = {
            ("Black","Kharif"):["Cotton","Soybean"],
            ("Red","Rabi"):["Groundnut","Wheat"],
            ("Sandy","Zaid"):["Watermelon","Cucumber"]
        }

        result = crops.get((soil,season),["Rice","Maize","Pulses"])

        st.success(f"✅ Recommended Crops: {', '.join(result)}")

# =====================================================
# DISEASE DETECTION
# =====================================================
elif page=="📸 Disease Detection":

    st.title("📸 AI Disease Detection")

    file = st.file_uploader("Upload Crop Image")

    if file:
        st.image(file,width=300)
        st.warning("AI Module Ready → Connect PlantVillage API for real detection.")

# =====================================================
# HUGE GOVERNMENT SCHEMES
# =====================================================
elif page=="🏛 Government Schemes":

    st.title("🏛 Farmer Welfare Schemes")

    schemes = [

        "PM-KISAN – ₹6000 yearly income support",
        "PMFBY – Crop insurance",
        "Soil Health Card – Free soil testing",
        "KCC – Low interest credit",
        "PKVY – Organic farming support",
        "Sub-Mission on Seeds",
        "National Beekeeping Initiative",
        "Blue Revolution – Fisheries",
        "Micro Irrigation Fund",
        "Agriculture Infrastructure Fund",
        "e-NAM digital marketplace",
        "Paramparagat Krishi Yojana",
        "Dairy Entrepreneurship Development",
        "Rashtriya Krishi Vikas Yojana",
        "National Food Security Mission"
    ]

    search = st.text_input("Search schemes...")

    for s in schemes:
        if search.lower() in s.lower():
            st.markdown(f'<div class="card">✅ {s}</div>',unsafe_allow_html=True)

# =====================================================
# WEATHER
# =====================================================
elif page=="🌦 Weather & Advisory":

    st.title("🌦 Smart Weather Advisory")

    st.info("🌤 28°C | Humidity: 60%")
    st.warning("Rain expected in 48 hrs — Delay pesticide spray.")

# =====================================================
# NOTIFICATIONS
# =====================================================
elif page=="🔔 Notifications":

    st.title("🔔 Alerts")

    st.success("Subsidy deadline approaching!")
    st.info("Market prices increased for pulses.")

# =====================================================
# ABOUT
# =====================================================
elif page=="ℹ️ About":

    st.title("About KisanSahay")

    st.write("""
KisanSahay is an AI-powered agricultural ecosystem designed to empower farmers with:

✅ AI advisory  
✅ Crop intelligence  
✅ Scheme awareness  
✅ Smart alerts  
✅ Disease detection  

Built for next-generation digital agriculture 🚀
""")

# =====================================================
# CONTACT
# =====================================================
elif page=="📞 Contact":

    st.title("Contact")

    st.write("📧 support@kisansahay.ai")
    st.write("☎ 1800-123-456")

    msg = st.text_area("Send us a message")

    if st.button("Submit"):
        st.success("We will contact you soon!")



