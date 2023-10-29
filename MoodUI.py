import requests
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(page_title="MoodUI", layout="wide")

# function to read the URL for the animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#----------LOAD ASSETS------------
lottie_coding = load_lottieurl("https://lottie.host/f7e1e0d6-3005-4c3b-86ec-dfce25385f01/sPjyphcf6W.json")

#----------FUNCTIONALITY----------
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;500;600;700&display=swap');
            </style>
            """, unsafe_allow_html=True)

        st.markdown("""
        <h1 style="font-family: 'Comfortaa';"> MoodTune </h1>
        """, unsafe_allow_html=True)
        st.write(" ")
        st.write("Hi, welcome to MoodTune. MoodTune is a music recommendation AI. Use MoodTune to find songs that relate to how you're feeling. Enjoy!")
    with right_column:
        st_lottie(lottie_coding, height=200, key="coding")
    st.write("---")

st.markdown("""
<style>
    .stTextInput>div>div>input {
        font-size: 16px;
        padding: 10px 15px;
        border: 2px solid #f63366;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

cols = st.columns([1, 2, 1])
with cols[1]:
    user_input = st.text_input("How are you feeling today? Describe your mood in a complete sentence.")
st.write(" ")

centered_cols = st.columns([1, 2, 1])
with centered_cols[1]:
    st.write("Click the Spotify button to continue...")
    spotify_url = "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"
    if st.button("Listen on Spotify"):
        st.write(f"Redirecting to Spotify...")
        st.markdown(f"<a href='{spotify_url}' target='_blank'>Click here if you're not redirected</a>", unsafe_allow_html=True)


