from IPython.display import display
import streamlit as st
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

def create_save_user_stories():          

    aws_region_name = os.getenv("aws_region_name")
    session = boto3.Session(profile_name=os.getenv("aws_local_vs_profile_name"))
    s3_client = session.client('s3')
    s3_bucket_name = os.environ["s3_pix_tales_bucket_name"]

    dynamodb = session.resource('dynamodb', region_name=aws_region_name) 
    dynamodb_table_name = os.environ["dynamodb_pix_tales_table"]
    table = dynamodb.Table(dynamodb_table_name)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    user_id = st.session_state.username
    story_id = "Story#" + current_time_str

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")   #'gemini-1.0-pro-vision-001'

    role = "You are a fascinating story teller who can write life stories of a person just by seeing his images at various ages."

    task = f"""You will be provided different images of same person. Along with the person's images, some description of that image may or may not be provided.
            If no descriptions are given about images provided, you can use your imagination to come up with interesting narration.
            If descriptions are given for images, you should use those descriptions along with your imagination to come up with fascinating life story.
            I want you to write a fascinating life story for a person whose images are given."""

    # File uploader and description input
    uploaded_pics = st.file_uploader(label="Pictures", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    story_title = st.text_input(label="Please provide title of the story")
    pics_description = st.text_area(label="Please provide description of pictures uploaded and anything else you want to mention about the person")

    instruction0 = f"Title of the story is {story_title} "

    content = [role, task, instruction0]

    submit_button = st.button(label="Generate Lifestory", key="GenLifeStory")

    # List to hold images
    pics_list = []
    pics_s3_urls = []
    is_error = 'N'
    
    if submit_button:
        
        if not story_title:
            st.error("Please input title of the story")
            is_error = 'Y'

        elif uploaded_pics != None:
            if len(uploaded_pics) > 10:
                st.error("You can only upload a maximum of 10 pictures.")
                is_error = 'Y'

        if is_error == 'N': 
            
            with st.spinner(text="Generating story. Please wait..."):
                for uploaded_pic in uploaded_pics:
                    
                    pic = PIL.Image.open(uploaded_pic)
                    pics_list.append(pic)

                    key = user_id + '/' + story_id + '/' + uploaded_pic.name
                    #TODO delete pics from S3 if LLM does not give response
                    s3_client.upload_file(
                        Filename = uploaded_pic.name,
                        Bucket = s3_bucket_name,
                        Key = key,
                        ExtraArgs={'ContentType': 'image/jpeg'}
                    )

                    url = f"https://{s3_bucket_name}.s3.{aws_region_name}.amazonaws.com/{key}"
                    pics_s3_urls.append(url) 


                # Add images and descriptions to content
                content.extend(pics_list)
                if pics_description:
                    content.append(pics_description)

                # Generate response from AI model
                response = "LLM Dummy Response" #model.generate_content(content)
                llm_text_response = "LLM Dummy Response" #response.text

                # Display results
                st.title(":blue[Lifestory] :sunglasses:")
                st.markdown(llm_text_response)

                #insert in dynamodb
                table.put_item(
                    Item = {
                        "PK": user_id,
                        "SK": story_id + "#InputUserData",
                        "UserId": user_id,
                        "StoryId": story_id,
                        "StoryTitle": story_title,
                        "ImagesURL": pics_s3_urls,
                        "ImagesDescr": pics_description,
                        "CreationTime": current_time_str
                    }
                    
                )

                table.put_item(
                    Item = {
                        "PK": user_id,
                        "SK": story_id + "#LLMData",
                        "UserId": user_id,
                        "StoryId": story_id,
                        "StoryTitle": story_title,
                        "LLMGenStory": llm_text_response,
                        "CreationTime": current_time_str
                    }
                )
                
                # Display uploaded images
                st.markdown("### Uploaded Pictures")
                cols = st.columns(len(pics_list))
                for col, img in zip(cols, pics_list):
                    col.image(img, use_column_width=True)

                st.success("Lifestory generated successfully!")

                social_media_links = [
                "https://www.facebook.com/",
                "https://www.youtube.com/",
                "https://www.instagram.com/",
                ]

                social_media_icons = SocialMediaIcons(social_media_links)

                social_media_icons.render()

                # Language in which you want to convert
                language = 'en'

                # Passing the text and language to the engine, 
                # here we have marked slow=False. Which tells 
                # the module that the converted audio should 
                # have a high speed
                #audio_filename = person_name + ".mp3"
                #audio_file = gTTS(text=llm_text_response, lang=language, slow=False)

                # Saving the converted audio in a mp3 file named
                #audio_file.save(audio_filename)

                #st.audio(audio_file, format='audio/mp3')

                # Footer
                st.markdown('<div style="text-align: center; margin-top: 50px; font-size: 14px; color: #888;">© 2024 Your Company. All rights reserved.</div>', unsafe_allow_html=True)

