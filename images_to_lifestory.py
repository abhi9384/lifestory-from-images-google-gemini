from IPython.display import display
import streamlit as st
import google.generativeai as genai
import PIL.Image
import numpy as np
from gtts import gTTS
import warnings
import os
from dotenv import load_dotenv

load_dotenv()

# Settings the warnings to be ignored 
warnings.filterwarnings('ignore') 

st.set_page_config(layout="wide", page_title="Lifestory from Images")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")   #'gemini-1.0-pro-vision-001'

role = "You are a fascinating story teller who can write life stories of a person just by seeing his images at various ages."

task = f"""You will be provided different images of same person. Along with the person's images, some description of that image may or may not be provided.
        If no descriptions are given about images provided, you can use your imagination to come up with interesting narration.
        If descriptions are given for images, you should use those descriptions along with your imagination to come up with fascinating life story.
        I want you to write a fascinating life story for a person whose images are given."""

# Sidebar inputs
st.sidebar.header("Input Details")
person_name = st.sidebar.text_input("Name of the person")
with st.sidebar:
       person_gender = st.radio("Gender of the person", ("Male", "Female"))

instruction0 = f"Name of the person is {person_name} and gender is {person_gender}. "

content = [role, task, instruction0]

# File uploader and description input
uploaded_pics = st.file_uploader(label="Pictures", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
pics_description = st.text_area(label="Please provide description of pictures uploaded and anything else you want to mention about the person")

submit_button = st.button(label="Generate Lifestory", key="GenLifeStory")

# List to hold images
pics_list = []

if submit_button:
    if uploaded_pics:
        for uploaded_pic in uploaded_pics:
            pic = PIL.Image.open(uploaded_pic)
            pics_list.append(pic)

        # Add images and descriptions to content
        content.extend(pics_list)
        if pics_description:
            content.append(pics_description)

        # Generate response from AI model
        response = model.generate_content(content)
        llm_text_response = response.text

        # Display results
        st.title(":blue[Lifestory] :sunglasses:")
        st.markdown("### Generated Lifestory")
        st.markdown(llm_text_response)
        
        # Display uploaded images
        st.markdown("### Uploaded Pictures")
        cols = st.columns(len(pics_list))
        for col, img in zip(cols, pics_list):
            col.image(img, use_column_width=True)

        st.success("Lifestory generated successfully!")

# Footer
st.markdown('<div style="text-align: center; margin-top: 50px; font-size: 14px; color: #888;">© 2024 Your Company. All rights reserved.</div>', unsafe_allow_html=True)
