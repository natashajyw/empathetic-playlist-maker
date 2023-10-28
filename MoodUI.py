import requests
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(page_title = "MoodUI", layout = "wide")

# function to read the URL for the animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
    
#----------LOAD ASSETS------------
# URL for the animation
lottie_coding = load_lottieurl("https://lottie.host/f7e1e0d6-3005-4c3b-86ec-dfce25385f01/sPjyphcf6W.json")

#----------FUNCTIONALITY----------
# Title/Description/Animation
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        # Import the Comfortaa font from Google Fonts
        st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;500;600;700&display=swap');
            </style>
            """, unsafe_allow_html=True)

        # Apply the Comfortaa font to your title using inline CSS
        st.markdown("""
        <h1 style="font-family: 'Comfortaa';"> MoodTune </h1>
        """, unsafe_allow_html=True)
        st.write(" ")
        st.write("Hi, welcome to MoodTune. MoodTune is a music recommendation AI. Use MoodTune to find songs that relate to how you're feeling. Enjoy!")
    with right_column:
        st_lottie(lottie_coding, height = 200, key = "coding")
    st.write("---")
# User Input
#  Custom CSS to center the textbox and style it
st.markdown("""
<style>
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 70vh;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
        padding: 10px 15px;
        border: 2px solid #f63366;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Center the textbox using new layout primitives
cols = st.columns([1, 2, 1])
with cols[1]:
    user_input = st.text_input("How are you feeling today? Describe your mood in a complete sentence")

# For formatting
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")

# Methodology/Credits
with st.container():
        st.header("Methodology")
        st.write("""
        1. Technologies used for UI: Python; StreamLit library and CSS.
        2. Hume.ai API used to apply concepts of Sentiment Analysis.
        3. Spotify API used to incorporate music recommendation algorithms.
        """)
