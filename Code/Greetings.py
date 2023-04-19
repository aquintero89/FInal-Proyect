import streamlit as st
import base64
from PIL import Image

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('WelcomeApp.jpg')


st.markdown(
    f'<h1 style="font-size: 80px; color: white">PlayPRO Analytics</h1>',
    unsafe_allow_html=True
)

st.markdown(
    f'<h3 style="color: white">Play to Win: Compare Players and Dominate the Game</h3>',
    unsafe_allow_html=True
)