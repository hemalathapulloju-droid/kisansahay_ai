import streamlit as st

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="KisanSense GenAI",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 KisanSense GenAI")
st.caption("AI-Powered Multilingual Agricultural Advisory Assistant")
st.divider()

# -------------------------------------------------
# LANGUAGE SELECTOR
# -------------------------------------------------
language = st.selectbox(
    "Select Language",
    ["English", "Telugu", "Hindi", "Tamil"]
)

# -------------------------------------------------
# AI ADVISORY LOGIC
# -------------------------------------------------
def agri_advice(q, lang):
    q = q.lower()

    responses = {
        "aphid": {
            "English": "Neem oil 3–5 ml per litre. Avoid excess nitrogen. Use Imidacloprid if infestation is severe.",
            "Telugu": "నీమ్ ఆయిల్ 3–5 మి.లీ లీటర్ నీటిలో పిచికారీ చేయాలి. అధిక నత్రజని నివారించండి.",
            "Hindi": "नीम तेल 3–5 मि.ली. प्रति लीटर पानी में छिड़कें। अधिक नाइट्रोजन से बचें।",
            "Tamil": "நீம் எண்ணெய் 3–5 மி.லி. ஒரு லிட்டர் தண்ணீரில் தெளிக்கவும்."
        },
        "fertilizer": {
            "English": "Apply balanced NPK based on soil test and crop stage.",
            "Telugu": "నేల పరీక్ష ఆధారంగా సమతుల్య NPK వాడాలి.",
            "Hindi": "मृदा परीक्षण के अनुसार संतुलित NPK का उपयोग करें।",
            "Tamil": "மண் பரிசோதனை அடிப்படையில் NPK பயன்படுத்தவும்."
        },
        "scheme": {
            "English": "PM-Kisan provides ₹6000 per year via direct benefit transfer.",
            "Telugu": "పీఎం-కిసాన్ ద్వారా సంవత్సరానికి ₹6000 లభిస్తుంది.",
            "Hindi": "पीएम किसान योजना से ₹6000 प्रति वर्ष मिलते हैं।",
            "Tamil": "PM-Kisan திட்டம் வருடத்திற்கு ₹6000 வழங்குகிறது."
        }
    }

    if "aphid" in q:
        return responses["aphid"][lang]

    if "fertilizer" in q:
        return responses["fertilizer"][lang]

    if "pm kisan" in q or "scheme" in q:
        return responses["scheme"][lang]

    fallback = {
        "English": "Please provide more details or consult your local agriculture officer.",
        "Telugu": "దయచేసి మరిన్ని వివరాలు ఇవ్వండి లేదా స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి.",
        "Hindi": "कृपया अधिक विवरण दें या स्थानीय कृषि अधिकारी से संपर्क करें।",
        "Tamil": "மேலும் விவரம் அளிக்கவும் அல்லது உள்ளூர் வேளாண் அதிகாரியை அணுகவும்."
    }

    return fallback[lang]

# -------------------------------------------------
# CHATBOT SESSION STATE
# -------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------------------------
# CHAT INPUT
# -------------------------------------------------
user_query = st.chat_input("Ask your farming question...")

if user_query:
    st.session_state.chat_history.append(("user", user_query))
    bot_reply = agri_advice(user_query, language)
    st.session_state.chat_history.append(("assistant", bot_reply))

# -------------------------------------------------
# DISPLAY CHAT
# -------------------------------------------------
for role, message in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").write(message)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.divider()
st.caption("KisanSense AI Engine | Multilingual • Explainable • Hackathon Ready 🌾")