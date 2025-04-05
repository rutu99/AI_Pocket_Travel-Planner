
#!pip install -q streamlit google-generativeai deep-translator pyngrok

#pip install streamlit langchain langchain-google-genai

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import random
from datetime import date
from deep_translator import GoogleTranslator

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
if not GOOGLE_API_KEY:
    st.error("⚠️ Google GenAI API key is missing! Please add it to `.streamlit/secrets.toml`.")
    st.stop()

def get_travel_options(source, destination):
    system_prompt = SystemMessage(
        content="You are an AI-powered travel assistant. Provide multiple travel options (cab, train, bus, flight) with estimated costs, duration, and relevant travel tips. Keep the interaction friendly and try to add travel friendly inspiring quotes in between make it look inspired to travel"
    )
    user_prompt = HumanMessage(
        content=f"I am traveling from {source} to {destination}. Suggest travel options with estimated cost, duration, and important details."
    )

    # ✅ Initialize AI model
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)

    try:
        response = llm.invoke([system_prompt, user_prompt])
        return response.content if response else "⚠️ No response from AI."
    except Exception as e:
        return f"❌ Error fetching travel options: {str(e)}"

st.title("🚀 AI-Powered Travel Planner")
st.markdown("Enter your travel details to get AI-generated travel options including cost estimates and travel tips.")

# ✅ User Inputs
source = st.text_input("🛫 Enter Source Location", placeholder="E.g., New York")
destination = st.text_input("🛬 Enter Destination", placeholder="E.g., Los Angeles")


from_date = st.date_input("📅 From Date", value=date.today())
to_date = st.date_input("📅 To Date", value=date.today())
# Updated Languages and Translations
LANGUAGES = {
    "English": "en",
    "Hindi (हिन्दी)": "hi",
    "Marathi (मराठी)": "mr",
    "Punjabi (ਪੰਜਾਬੀ)": "pa",
    "Gujarati (ગુજરાતી)": "gu",
    "Bengali (বাংলা)": "bn"
}

# Translations for "Travel Recommendations:"
HEADINGS_TRANSLATION = {
    "English": "📍 Travel Recommendations:",
    "Hindi (हिन्दी)": "📍 यात्रा अनुशंसाएँ:",
    "Marathi (मराठी)": "📍 प्रवास शिफारशी:",
    "Punjabi (ਪੰਜਾਬੀ)": "📍 ਯਾਤਰਾ ਸਿਫ਼ਾਰਸ਼ਾਂ:",
    "Gujarati (ગુજરાતી)": "📍 પ્રવાસ સૂચનો:",
    "Bengali (বাংলা)": "📍 ভ্রমণ সুপারিশ:"
}

TRANSLATION_LIMIT = 5000

selected_lang = st.selectbox("🌐 Choose Language for Output", list(LANGUAGES.keys()))
translate_output = st.checkbox("🌍 Translate output to selected language")

# 🔍 Travel Recommendation Button

if st.button("🔍 Find Travel Options"):
    if source.strip() and destination.strip():
        with st.spinner("🔄 Fetching best travel options..."):
            # Inject dates into user prompt for better results
            travel_info = get_travel_options(
                source, destination + f" from {from_date} to {to_date}"
            )
            st.success("✅ Travel Recommendations:")
            st.markdown(travel_info)

            if translate_output and selected_lang != "English":
                try:
                    translated = GoogleTranslator(source='auto', target=LANGUAGES[selected_lang]).translate(travel_info[:TRANSLATION_LIMIT])
                    st.markdown(f"**{HEADINGS_TRANSLATION[selected_lang]}**")
                    st.markdown(translated)
                except Exception as e:
                    st.error(f"⚠️ Error translating: {e}")
    else:
        st.warning("⚠️ Please enter both source and destination locations.")
