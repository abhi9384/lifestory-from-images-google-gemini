from IPython.display import display
import streamlit as st
from streamlit_navigation_bar import st_navbar
from app_pages.create_user_stories import create_save_user_stories
from app_pages.view_user_saved_stories import view_user_stories
from app_pages.search_stories import search_all_stories
from st_social_media_links import SocialMediaIcons
import google.generativeai as genai
import PIL.Image
import numpy as np
from gtts import gTTS
import boto3
from datetime import datetime
import warnings
import os
from dotenv import load_dotenv

load_dotenv()

# Settings the warnings to be ignored 
warnings.filterwarnings('ignore') 

st.set_page_config(layout="wide", page_title="Lifestory from Images", initial_sidebar_state="expanded")

st.sidebar.title("Login Page")
st.sidebar.header("Register/Login")

# Simulate a simple user authentication
def authenticate(username, password):
    #TODO add aws cognito
    return username == "abhi" and password == "password"

# Login Page
def login_page():

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    with st.sidebar:
        if st.sidebar.button("Login", key="Login"):
    
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.sidebar.write('<b>Logged in User: ' + st.session_state.username + '</b>', unsafe_allow_html=True)
            else:
                st.sidebar.error("Invalid username or password.")

def post_login():
    
    pages = ["Create Your Story", "View Your Stories", "Search Stories"]
    styles = {
        "nav": {
                "background-color": "royalblue",
        },
        "div": {
            "max-width": "32rem",
        },
        "span": {
            "border-radius": "0.5rem",
            "color": "rgb(49, 51, 63)",
            "margin": "0 0.125rem",
            "padding": "0.4375rem 0.625rem",
        },
        "active": {
            "background-color": "rgba(255, 255, 255, 0.25)",
        },
        "hover": {
            "background-color": "rgba(255, 255, 255, 0.35)",
        },
    }

    page = st_navbar(pages, styles=styles)
    st.title("_PixTales_ :sunglasses: Your story generator")
    
    functions = {
    "Create Your Story": create_save_user_stories,
    "View Your Stories": view_user_stories,
    "Search Stories": search_all_stories
    }

    go_to = functions.get(page)
    if go_to:
        go_to()

# Main app function
def main():

    if 'authenticated' not in st.session_state:
        login_page()

    if 'authenticated' in st.session_state:
        post_login()

if __name__ == "__main__":
    main()