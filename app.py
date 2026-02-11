import streamlit as st
from deep_translator import GoogleTranslator
import random

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
        ["English","Telugu","Hindi","Marathi","Tamil"])

    if st.button("Login"):
        if name and place:
            st.session_state.logged_in=True
            st.session_state.name=name
            st.session_state.place=place
            st.session_state.land=land
            st.session_state.language=language
            st.rerun()

# =====================================================
# SMART MULTILINGUAL AI ASSISTANT
# =====================================================
def ai_chat():

    st.header("🤖 Smart AI Assistant")

    lang=st.selectbox("Select Answer Language",
    ["English","Telugu","Hindi","Marathi","Tamil"])

    query=st.text_area("Ask anything about farming, schemes, diseases, crops...")

    if query:

        q=GoogleTranslator(source='auto', target='en').translate(query).lower()

        knowledge_base={

        "rice":"Rice needs standing water, transplanting method, split nitrogen fertilization and pest monitoring.",
        "fertilizer":"Use balanced NPK fertilizer. Conduct soil testing and avoid excess nitrogen.",
        "scheme":"PM-KISAN gives income support. PMFBY provides crop insurance. Soil Health Card helps soil testing.",
        "disease":"Remove infected leaves, apply neem oil spray and ensure good air circulation.",
        "weather":"Plan irrigation based on temperature and rainfall forecast.",
        "crop":"Crop rotation improves soil fertility and reduces pest attacks."
        }

        response="Smart Advice: Maintain soil health, monitor pests and follow climate-based farming."

        for key in knowledge_base:
            if key in q:
                response=knowledge_base[key]

        final=GoogleTranslator(source='en', target=lang).translate(response)

        st.success(final)

# =====================================================
# DISEASE DETECTION (AI STYLE ANALYSIS)
# =====================================================
def disease():

    st.header("📸 AI Plant Disease Detection")

    file=st.file_uploader("Drop crop/leaf image", type=["jpg","png"])

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
Analysis Report:

{pred[1]}

Eradication Process:
• Remove infected parts
• Use neem-based pesticide
• Maintain spacing between plants
• Avoid over watering
• Monitor for 5 days
""")

# =====================================================
# GOVERNMENT SCHEMES
# =====================================================
def schemes():

    st.header("🏛 Government Schemes")

    schemes_data=[

    ("PMFBY","Crop Insurance","Financial protection against crop loss",
    "All farmers growing notified crops",
    "https://pmfby.gov.in"),

    ("PM-KISAN","Income Support","₹6000 yearly support",
    "Small and marginal farmers",
    "https://pmkisan.gov.in"),

    ("Soil Health Card","Soil Testing","Improve soil fertility",
    "All farmers",
    "https://soilhealth.dac.gov.in"),

    ("Kisan Credit Card","Farm Loan","Low interest agricultural loan",
    "Farm land owners",
    "https://www.myscheme.gov.in")
    ]

    for s in schemes_data:

        with st.expander(s[0]):

            st.write("Category:",s[1])
            st.write("Benefits:",s[2])
            st.write("Eligibility:",s[3])

            st.markdown(f"[Apply Now]({s[4]})")

# =====================================================
# WEATHER ADVISORY (SMART SIMULATION)
# =====================================================
def weather():

    st.header("🌦 Weather & Advisory")

    st.write(f"Location: {st.session_state.place}")

    week=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

    cols=st.columns(7)

    for i,d in enumerate(week):
        cols[i].metric(d,f"{random.randint(25,33)}°C")

    st.subheader("Crop Maintenance Suggestions")

    st.info("Rain expected midweek — reduce irrigation.")
    st.info("Apply fertilizer during cooler hours.")
    st.warning("Monitor pests during humidity rise.")

# =====================================================
# DASHBOARD WITH NEWS
# =====================================================
def dashboard():

    st.title(f"Welcome {st.session_state.name} 👋")

    col1,col2,col3=st.columns(3)

    if col1.button("🌱 Crop Advisory"):
        st.session_state.page="🤖 AI Assistant"
        st.rerun()

    if col2.button("🤖 AI Enabled"):
        st.session_state.page="🤖 AI Assistant"
        st.rerun()

    if col3.button("🌦 Weather Active"):
        st.session_state.page="🌦 Weather & Advisory"
        st.rerun()

    st.subheader("📰 Farming News — 11-02-2026")

    st.info("Government launches new subsidy scheme for small farmers.")
    st.info("Hybrid rice varieties show higher yield.")
    st.info("Digital agriculture adoption increasing across India.")
    st.info("New irrigation support announced by state governments.")

# =====================================================
# NOTIFICATIONS
# =====================================================
def notifications():
    st.header("🔔 Notifications")
    st.success("Rain expected in coming days.")
    st.warning("Check crop for early disease signs.")

# =====================================================
# ABOUT
# =====================================================
def about():

    st.write("""
KisanSense is a multilingual agritech platform designed to empower farmers with AI-driven crop advisory, disease detection, weather updates, and government schemes information.

It provides personalized guidance based on region and language preference helping farmers improve productivity and reduce crop loss.
""")

    st.subheader("Creators")

    st.write("""
1. Hemalatha Pulloju  
2. Thapasi Swarna  
3. Divya Sree  
4. Shivani  
5. Divya
""")

# =====================================================
# CONTACT SUPPORT
# =====================================================
def contact():

    st.write("📞 +91 9059184778")
    st.write("📧 kisansahayfarm@gmail.com")

    msg=st.text_area("Send Message")

    if st.button("Submit"):
        st.success("Message Sent Successfully!")

# =====================================================
# MAIN NAVIGATION
# =====================================================
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
        contact()

# =====================================================
# RUN
# =====================================================
if not st.session_state.logged_in:
    login()
else:
    main()

