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

add_bg_from_local('Images/ChampionsWP.jpeg')

st.markdown(
    f'<h1 style="font-size: 60px; color: white; cursive;">About</h1>',
    unsafe_allow_html=True
)

st.markdown(
    f'<h3 style="color: white; font-weight: normal;">PlayPRO Analytics is a Streamlit app that uses KMeans clustering to group football players based on their attributes in FIFA 22. The user can input the name of a football player from a dataset consisting of more than 18,000 players, and the app will display their attributes and suggest 5 other similar players based on their attributes.</h3>',
    unsafe_allow_html=True
)

image_path = "Images/Dabball.png"

st.image(image_path)