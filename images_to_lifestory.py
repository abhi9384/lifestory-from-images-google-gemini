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
        I want you to write a fascinating life story for a person whose images are given in 100 words or less."""

person_name = st.sidebar.text_input("Name of the person")
with st.sidebar:
       person_gender = st.radio("Gender of the person", ("Male", "Female"))

instruction0 = f"Name of the person is {person_name} and gender is {person_gender}. "

content = [role, task, instruction0]

uploaded_pics = st.file_uploader(label="Picture 1", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
pics_description = st.text_area(label="Please provide description of pictures uploaded and anything else you want to mention about the person")

submit_button = st.button(label="Generate Lifestory", key="GenLifeStory")

pics_list = []

if submit_button:

        #st.write('No of pics uploaded: ', len(uploaded_pics))

        for uploaded_pic in uploaded_pics:
                pic = PIL.Image.open(uploaded_pic)
                #st.image(pic) # to display image
                
                pics_list.append(pic)
        
        #st.write('pics_list: ', pics_list)
        for item in pics_list:
                 if item!= None:
                         content.append(item)

        if pics_description != None:
               content.append(pics_description)

        response = model.generate_content(content)
        llm_text_response = response.text

        st.title(":blue[Lifestory] :sunglasses:")

        with st.container():
                st.markdown(llm_text_response)




# Language in which you want to convert
#language = 'en'

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
#audio_file = gTTS(text=llm_text_response, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
#audio_file.save("Elly.mp3")
