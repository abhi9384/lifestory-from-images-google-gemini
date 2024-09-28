from IPython.display import display
from dotenv import load_dotenv
import google.generativeai as genai
import os
import PIL.Image
from gtts import gTTS
import warnings

load_dotenv()

# Settings the warnings to be ignored 
warnings.filterwarnings('ignore') 

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")   #'gemini-1.0-pro-vision-001'

role = "You are a fascinating story teller who can write life stories of a person just by seeing his images at various ages."

task = f"""You will be provided different images of same person. Along with the person's images, some description of that image may or may not be provided.
        If no descriptions are given about images provided, you can use your imagination to come up with interesting narration.
        If descriptions are given for images, you should use those descriptions along with your imagination to come up with fascinating life story.
        I want you to write a fascinating life story for a person whose images are given."""

instruction1 = "Please write a story about a young girl. Her name is Elly. She was born in Singapore. Her pic when she was born: "
pic1 = PIL.Image.open("IMG-20151222-WA0003.jpg")

instruction2 = "Her picture at the age of 1.5 years in Malaysia Hotel during vacation: "
pic2 = PIL.Image.open('IMG_0083.JPG')

instruction3 = "Her picture at the age of 3 years on her first cruise trip to Bali from Singapore: "
pic3 = PIL.Image.open('IMG_0764.JPG')

instruction4 = "Her picture at the age of 4.5 years in her first school's Father's day celebration: "
pic4 = PIL.Image.open('FRSA4569.JPG')

content = [role, task, instruction1, pic1, instruction2, pic2, instruction3, pic3, instruction4, pic4]

response = model.generate_content(content)
llm_text_response = response.text
print("Lifestory: ", llm_text_response)

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
audio_file = gTTS(text=llm_text_response, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
audio_file.save("Elly.mp3")