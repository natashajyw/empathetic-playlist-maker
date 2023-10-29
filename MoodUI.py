# MoodUI.py
import requests
import streamlit as st
from streamlit_lottie import st_lottie

# main
import asyncio

from enum import Enum
from hume import HumeStreamClient
from hume.models.config import LanguageConfig

st.set_page_config(page_title="MoodUI", layout="wide")

### Start of main global vars ###
samples = []

attribute_list = [[0.0 for i in range(4)] for j in range(3)]

class MusAttribute(Enum):
    ENERGY = 0
    LIVENESS = 1
    LOUDNESS = 2
    TEMPO = 3

### end main global vars ###

###### main stuff #####
async def CallHume():
    client = HumeStreamClient("7kBEBKHVRNGmYD4OQfIusARM8g40nvEGf5cXpUiAeohJZhCE")
    config = LanguageConfig()
    async with client.connect([config]) as socket:
        for sample in samples:
            result = await socket.send_text(sample)
            emotions = result["language"]["predictions"][0]["emotions"]
            return emotions

async def DetermineAttributes():
    list = await CallHume()
    values_to_keep = ['Anger', 'Anxiety', 'Calmness', 'Distress', 'Ecstasy', 'Enthusiasm', 'Excitement', 'Joy', 'Sadness']

    emotion_list = [item for item in list if item['name'] in values_to_keep]

    emotion_list = sorted(emotion_list, key=lambda x: x['score'], reverse=True)
    emotion_list = emotion_list[:3]

    for item in emotion_list:
        print(item)

    for i in range(3):
        if emotion_list[i]['name'] == 'Anger' or emotion_list[i]['name'] == 'Distress' or emotion_list[i]['name'] == 'Anxiety' or emotion_list[i]['name'] == 'Calmness':
            attribute_list[i][MusAttribute['ENERGY'].value] = 0.3
            attribute_list[i][MusAttribute['LIVENESS'].value] = 0.3
            attribute_list[i][MusAttribute['LOUDNESS'].value] = 0.4
            attribute_list[i][MusAttribute['TEMPO'].value] = 60
        elif emotion_list[i]['name'] == 'Ecstasy' or emotion_list[i]['name'] == 'Joy' or emotion_list[i]['name'] == 'Excitement' or emotion_list[i]['name'] == 'Enthusiasm':
            attribute_list[i][MusAttribute['ENERGY'].value] = 0.8
            attribute_list[i][MusAttribute['LIVENESS'].value] = 0.8
            attribute_list[i][MusAttribute['LOUDNESS'].value] = 0.8
            attribute_list[i][MusAttribute['TEMPO'].value] = 150
        elif emotion_list[i]['name'] == 'Sadness':
            attribute_list[i][MusAttribute['ENERGY'].value] = 0.1
            attribute_list[i][MusAttribute['LIVENESS'].value] = 0.2
            attribute_list[i][MusAttribute['LOUDNESS'].value] = 0.5
            attribute_list[i][MusAttribute['TEMPO'].value] = 70

    for item in attribute_list:
        print(item)

def ReturnMusAttribute():
    return attribute_list;
# end main

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
    st.write("Click on the button below to continue:")
    spotify_url = "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"
    if st.button("Make me a Spotify playlist!"):
        st.write(f"Redirecting to Spotify...")
        samples.append(user_input) # adding user input to samples list
        asyncio.run(DetermineAttributes()) # Run DetermineAttributes withint asyncio
        st.markdown(f"<a href='{spotify_url}' target='_blank'>Click here if you're not automatically redirected</a>", unsafe_allow_html=True)


