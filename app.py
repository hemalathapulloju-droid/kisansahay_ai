import streamlit as st
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(page_title="KisanSahay", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);}
h1,h2,h3,h4,p,label {color:white !important;}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= LOGIN =================
def login():
    st.title("🌾 KisanSahay Farmer Login")
    name = st.text_input("Farmer Name")
    place = st.text_input("Village / City")

    if st.button("Login"):
        if name and place:
            st.session_state.logged_in = True
            st.session_state.name = name
            st.session_state.place = place
            st.rerun()
        else:
            st.warning("Please enter name and place to continue.")

# ================= LANGUAGE MAP =================
lang_map = {
    "English":"en",
    "Telugu":"te",
    "Hindi":"hi",
    "Marathi":"mr",
    "Tamil":"ta"
}

# ================= SMART AI =================
def smart_ai(q, lang):
    """
    Generate AI answer in paragraph style, in the specified language.
    """
    query = q.lower()

    # Base answer in English
    if "rice" in query:
        ans = ("Rice farming involves several key steps to ensure a healthy crop yield. "
               "Farmers should prepare the nursery, maintain proper water levels, "
               "apply fertilizers carefully, and monitor for pests and diseases regularly.")
    elif "scheme" in query:
        ans = ("There are several government schemes to support farmers. "
               "PM-Kisan provides financial assistance, PMFBY offers crop insurance, "
               "Kisan Credit Card provides low-interest loans, Soil Health Card monitors soil quality, "
               "and irrigation subsidies support efficient water usage.")
    elif "disease" in query:
        ans = ("To detect and treat plant diseases, farmers can observe symptoms carefully "
               "and follow preventive measures. For example, neem oil sprays, removing infected leaves, "
               "and maintaining proper soil health can reduce crop loss.")
    else:
        ans = ("Farmers should follow seasonal crop planning, regularly test soil, "
               "apply balanced fertilizers, and monitor crops for pests and diseases. "
               "These practices ensure sustainable and productive farming.")

    # Hardcoded translations
    translations = {
        "English": ans,
        "Telugu": "ధాన్యం సాగులో మంచి దిగుబడి కోసం కొన్ని ముఖ్యమైన దశలు ఉన్నాయి. రైతులు నర్సరీని సిద్ధం చేయాలి, నీటి స్థాయిని సరిపడుగా ఉంచాలి, ఎరువులను జాగ్రత్తగా ఉపయోగించాలి, మరియు పురుగు మరియు రోగాలను రెగ్యులర్‌గా పరిశీలించాలి.",
        "Hindi": "चावल की खेती में अच्छे उत्पादन के लिए कई महत्वपूर्ण कदम होते हैं। किसानों को नर्सरी तैयार करनी चाहिए, पानी का स्तर बनाए रखना चाहिए, उर्वरकों का सावधानीपूर्वक उपयोग करना चाहिए, और कीट और रोगों की नियमित निगरानी करनी चाहिए।",
        "Marathi": "भात लागवडीत चांगल्या उत्पन्नासाठी काही महत्वाच्या पायऱ्या आहेत. शेतकऱ्यांनी नर्सरी तयार करावी, पाण्याची योग्य पातळी राखावी, खत काळजीपूर्वक वापरावे आणि कीटक व रोग यांचे नियमित निरीक्षण करावे.",
        "Tamil": "அரிசி விவசாயத்தில் நல்ல அறுவடை பெற சில முக்கிய படிகள் உள்ளன. விவசாயிகள் நர்சரி தயார் செய்ய வேண்டும், நீர் நிலையை சரியாக பராமரிக்க வேண்டும், உரங்களை கவனமாக பயன்படுத்த வேண்டும் மற்றும் பூச்சிகள் மற்றும் நோய்களை முறையாக கண்காணிக்க வேண்டும்."
    }

    return translations.get(lang, ans)

# ================= SIMULATED WEATHER =================
def weather():
    st.header("🌦 Current Weather Advisory")
    city = st.session_state.place
    today = datetime.today().strftime("%d-%m-%Y")

    # Simulated weather data
    temp = "32°C"
    humidity = "60%"
    condition = "Partly cloudy"

    # Display image based on condition
    weather_images = {
        "sunny": "https://images.unsplash.com/photo-1501973801540-537f08ccae7b",
        "cloudy": "https://images.unsplash.com/photo-1529864724933-cb37c5da8f80",
        "rainy": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d",
        "storm": "https://images.unsplash.com/photo-1502920514313-52581002a659"
    }

    img_url = weather_images["cloudy"]  # Example: cloudy
    st.image(img_url, width=400)
    st.write(f"**City:** {city}")
    st.write(f"**Date:** {today}")
    st.write(f"**Temperature:** {temp}")
    st.write(f"**Humidity:** {humidity}")
    st.write(f"**Condition:** {condition}")

# ================= NEWS =================
def news():
    st.header("📰 Agriculture News India")
    today = datetime.today().strftime("%d-%m-%Y")

    st.image("https://images.unsplash.com/photo-1598514982306-7a4cf2f4c43c", width=400)
    st.write(today, "New fertilizer subsidy announced.")
    st.markdown("[Read More](https://www.thehindu.com)")

    st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef", width=400)
    st.write(today, "AI technology improving Indian farming.")
    st.markdown("[Read More](https://indianexpress.com)")

# ================= SCHEMES =================
def schemes():
    st.header("🏛 Government Schemes")
    schemes_data = [
        ("PM-Kisan","Small farmers","₹6000 yearly","https://pmkisan.gov.in/"),
        ("PMFBY","Crop insurance","Protection against crop loss","https://pmfby.gov.in/"),
        ("Soil Health Card","All farmers","Free soil testing","https://soilhealth.dac.gov.in/"),
        ("Kisan Credit Card","Land farmers","Low interest loans","https://www.myscheme.gov.in"),
        ("PMKSY Irrigation","Irrigation farmers","Water subsidy","https://pmksy.gov.in/"),
        ("eNAM","All farmers","Online market access","https://www.enam.gov.in/")
    ]
    for s in schemes_data:
        st.subheader(s[0])
        st.write("Eligibility:", s[1])
        st.write("Benefit:", s[2])
        st.markdown(f"[Apply]({s[3]})")

# ================= DISEASE =================
def disease():
    st.header("📸 AI Disease Detection")
    file = st.file_uploader("Upload plant image")
    if file:
        st.success("Leaf Spot detected")
        st.write("Treatment: Neem oil spray, remove infected leaves.")

# ================= AI CHAT =================
def chatbot():
    st.header("🤖 Smart AI Assistant")
    lang = st.selectbox("Select Language", ["English","Telugu","Hindi","Marathi","Tamil"])
    question = st.text_area("Ask your farming question")
    if st.button("Submit Question"):
        if question:
            answer = smart_ai(question, lang)
            st.subheader("AI Response")
            st.success(answer)
        else:
            st.warning("Please type a question.")

# ================= DASHBOARD =================
def dashboard():
    st.title(f"Welcome {st.session_state.name} 👋")
    col1, col2, col3 = st.columns(3)
    if col1.button("🌱 Crop Advisory"):
        chatbot()
    if col2.button("🤖 AI Assistant"):
        chatbot()
    if col3.button("🌦 Weather"):
        weather()
    news()

# ================= MAIN =================
def main():
    page = st.sidebar.radio("Navigation",
        ["🏠 Dashboard","🤖 AI Assistant","📸 Disease Detection",
         "🏛 Government Schemes","🌦 Weather","ℹ️ About","📞 Contact"])

    if page=="🏠 Dashboard":
        dashboard()
    elif page=="🤖 AI Assistant":
        chatbot()
    elif page=="📸 Disease Detection":
        disease()
    elif page=="🏛 Government Schemes":
        schemes()
    elif page=="🌦 Weather":
        weather()
    elif page=="ℹ️ About":
        st.write("""
KisanSense is a multilingual agritech platform designed to empower farmers 
with AI-driven crop advisory, disease detection, weather updates, 
and information on government schemes.

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


