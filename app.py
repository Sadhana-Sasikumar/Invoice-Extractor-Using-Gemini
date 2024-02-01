## Invoice Extractor

from dotenv import load_dotenv

load_dotenv() #to load all the env variables from .env

import streamlit as st
import os #to get the env variable 
from PIL import Image #to get the info from the image 
import google.generativeai as genai 

#Configuring api key
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#function to load the gemini pro vision model and get response

def get_gemini_response(input,image,prompt): #input will be the message that the llm modle will behave and prompt is my input giving wht kind of info i want
   #loading the genai model
    model = genai.GenerativeModel('gemini-pro-vision') 
    response =model.generate_content([input,image[0],prompt]) #image will be in the form of list
    return response.text

def input_image_setup(uploaded_file):
     # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input") #input box what specific input i want will be sent here
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"]) #file uploader acceptable formats if you want pdf add it here
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True) #displays the image after it has been uploaded


submit=st.button("Tell me about the image") #submit button   

#prompt template-how the google gemini pro must behave
input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

## If ask button is clicked

if submit:
    #the img data is now got into image_data
    image_data = input_image_setup(uploaded_file) 
    #and sent to gemini for the reponse, the input prompt is mentioned above and the input will be got from the user using text box
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)


