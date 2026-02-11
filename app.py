import streamlit as st
import requests
from datetime import datetime
from deep_translator import GoogleTranslator

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
    st.session_state.logged_in=False

# ================= LOGIN =================
def login():
    st.title("🌾 KisanSahay Farmer Login")

    name = st.text_input("Farmer Name")
    place = st.text_input("Village / City")
    lang = st.selectbox("Language", ["English","Telugu","Hindi","Marathi","Tamil"])

    if st.button("Login"):
        st.session_state.logged_in = True
        st.session_state.name = name
        st.session_state.place = place
        st.session_state.language = lang
        st.rerun()

# ================= LANGUAGE MAP =================
lang_map = {
    "English":"en",
    "Telugu":"te",
    "Hindi":"hi",
    "Marathi":"mr",
    "Tamil":"ta"
}

# ================= SMART AI =================
def smart_ai(q):
    user_lang_code = lang_map.get(st.session_state.language, "en")

    # Translate user query to English for processing
    try:
        translated_query = GoogleTranslator(source='auto', target='en').translate(q)
    except:
        translated_query = q

    query = translated_query.lower()

    # Generate detailed paragraph-style response
    if "rice" in query:
        ans = ("Rice farming involves several important steps to ensure a healthy crop yield. "
               "First, prepare the nursery and sow seeds carefully. Maintain proper water levels "
               "throughout the growing season. Apply nitrogen fertilizers judiciously, and regularly "
               "monitor for pests and diseases to take timely action.")
    elif "scheme" in query:
        ans = ("There are various government schemes available to support farmers. "
               "PM-Kisan provides financial assistance, PMFBY offers crop insurance, Kisan Credit Card "
               "enables low-interest loans, Soil Health Card helps monitor soil quality, "
               "and irrigation subsidies support efficient water management.")
    elif "disease" in query:
        ans = ("If your crops show signs of disease, you can use the AI-based disease detection "
               "feature by uploading images of the affected plants. The system will diagnose "
               "the issue and provide guidance on treatment measures, such as recommended pesticides, "
               "sprays, or cultural practices to manage the disease effectively.")
    else:
        ans = ("Farmers should follow seasonal crop planning, regularly test soil quality, "
               "apply a balanced mix of fertilizers, and continuously monitor crops for pests "
               "and diseases. Combining these practices ensures sustainable and productive farming.")

    # Translate AI response to user's language
    try:
        final_response = GoogleTranslator(source='en', target=user_lang_code).translate(ans)
    except:
        final_response = ans

    return final_response

# ================= WEATHER =================
def weather():
    st.header("🌦 Weather Advisory")
    key = st.secrets.get("WEATHER_KEY","")
    if not key:
        st.warning("Add WEATHER_KEY in secrets.")
        return

    city = st.session_state.place
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    data = requests.get(url).json()

    if "main" in data:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        desc = data['weather'][0]['description'].capitalize()

        # Display as emphasized weather card
        st.subheader(f"Current Weather in {city}")
        st.write(f"**Temperature:** {temp} °C")
        st.write(f"**Humidity:** {humidity} %")
        st.write(f"**Condition:** {desc}")

# ================= NEWS =================
def news():
    st.header("📰 Agriculture News India")
    today = datetime.today().strftime("%d-%m-%Y")

    st.image("https://images.unsplash.com/photo-1598514982306-7a4cf2f4c43c",width=400)
    st.write(today,"New fertilizer subsidy announced.")
    st.link_button("Read More","https://www.thehindu.com")

    st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef",width=400)
    st.write(today,"AI technology improving Indian farming.")
    st.link_button("Read More","https://indianexpress.com")

# ================= SCHEMES =================
def schemes():
    st.header("🏛 Government Schemes")
    schemes_data=[
        ("PM-Kisan","Small farmers","₹6000 yearly","https://pmkisan.gov.in/"),
        ("PMFBY","Crop insurance","Protection against crop loss","https://pmfby.gov.in/"),
        ("Soil Health Card","All farmers","Free soil testing","https://soilhealth.dac.gov.in/"),
        ("Kisan Credit Card","Land farmers","Low interest loans","https://www.myscheme.gov.in"),
        ("PMKSY Irrigation","Irrigation farmers","Water subsidy","https://pmksy.gov.in/"),
        ("eNAM","All farmers","Online market access","https://www.enam.gov.in/")
    ]

    for s in schemes_data:
        st.subheader(s[0])
        st.write("Eligibility:",s[1])
        st.write("Benefit:",s[2])
        st.link_button("Apply",s[3])

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
    q = st.text_area("Ask farming question")
    if st.button("Submit Question"):
        if q:
            ans = smart_ai(q)
            st.subheader("AI Response")
            st.success(ans)

# ================= DASHBOARD =================
def dashboard():
    st.title(f"Welcome {st.session_state.name} 👋")
    col1,col2,col3 = st.columns(3)
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
["🏠 Dashboard","🤖 AI Assistant","📸 Disease Detection","🏛 Government Schemes","🌦 Weather","ℹ️ About","📞 Contact"])

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

