from IPython.display import display
import streamlit as st
from st_social_media_links import SocialMediaIcons
import google.generativeai as genai
import PIL.Image
import numpy as np
from gtts import gTTS
import boto3 
from boto3.dynamodb.conditions import Key
from datetime import datetime
import warnings
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

aws_region_name = os.getenv("aws_region_name")
session = boto3.Session(profile_name=os.getenv("aws_local_vs_profile_name"))
dynamodb = session.resource('dynamodb', region_name=aws_region_name) 
dynamodb_table_name = os.environ["dynamodb_pix_tales_table"]
table = dynamodb.Table(dynamodb_table_name)

s3_client = session.client('s3')
s3_bucket_name = os.environ["s3_pix_tales_bucket_name"]


def delete_user_story(userid, storyid):

    #delete from s3
    folder_name = userid + '/' + storyid
    # List and delete all objects in the specified folder
    response = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix=folder_name)
    
    if 'Contents' in response:
        for obj in response['Contents']:
            s3_client.delete_object(Bucket=s3_bucket_name, Key=obj['Key'])

    #delete from Dynamodb
    
    response = table.delete_item(
        Key={
            'PK': userid,
            'SK': storyid  + "#InputUserData"
        }
    )

    response = table.delete_item(
        Key={
            'PK': userid,
            'SK': storyid  + "#LLMData"
        }
    )        
    

    st.write('<b>This story is deleted. It wont be visible in future. </b>', unsafe_allow_html=True)

def view_user_stories(): 

    # resp = table.query(
    #     TableName = 'User-Pix-Tales',
    #     KeyConditionExpression = "PK=:pk",
    #         ExpressionAttributeValues = {
    #             ':pk': {'S': 'abhi'}
    #         }
    #      )
    response = table.query(
       KeyConditionExpression=Key('PK').eq('abhi')
    )

    items = response.get('Items', [])
    
    if len(items) != 0:       # to check if dict is not empty

        for count, item in enumerate(items):

            with st.container():

                # Custom CSS for the Streamlit container
                st.markdown("""
                <style>
                    .stContainer {
                        "background-color": "royalblue",
                        border-radius: 10px;         /* Rounded corners */
                        padding: 20px;                /* Padding inside the container */
                        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); /* Shadow effect */
                    }
                    
                    }
                </style>
                """, unsafe_allow_html=True)
        
                if count%2 == 0:    #as ddb table has two records for each story: input user data and llm data
                    st.markdown(f"<div style='color: blue; font-size: 18px;'>Story Created On: " + item["CreationTime"] + "</div>", unsafe_allow_html=True)
                    delete_button = st.button(label="Delete this Story", key='DeleteButton' + item["PK"] + item["StoryId"])
                    if delete_button:
                        delete_user_story(item["PK"], item["StoryId"])

                if 'ImagesDescr' in item:
                    st.write('<b>Story Title: </b>' + item["StoryTitle"], unsafe_allow_html=True)
                    st.write('<b>Story Description: </b>' + item["ImagesDescr"], unsafe_allow_html=True)
                
                if 'LLMGenStory' in item:
                    st.write('<b>Generated Story: </b>' + item["LLMGenStory"], unsafe_allow_html=True)

                if 'ImagesURL' in item:

                    for img in item["ImagesURL"]:
                        
                        key = img.replace(f"https://{s3_bucket_name}.s3.{aws_region_name}.amazonaws.com/", " ")

                        #st.write("Key: " + key)

                        presigned_url = s3_client.generate_presigned_url(
                            ClientMethod='get_object',
                            ExpiresIn=60, 
                            Params={
                                'Bucket': s3_bucket_name,
                                'Key': key, 
                                'ResponseContentType': 'image/jpeg'
                            }
                        )
                        #st.write(presigned_url)
                        #st.image(presigned_url)
                
        st.write(items)

    else:
        st.markdown('<b>You have not created any stories</b>', unsafe_allow_html=True)
        