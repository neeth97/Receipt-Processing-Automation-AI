import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai
import pdfplumber
import io

#load environment varibles
load_dotenv()
#configuration google gemini
genai.configure(api_key="AIzaSyALzGUffR57uvQoIR4PMpVsn4Vpw9QiXP0")

model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input_text,image=None):
    if image is None:
        rsponse=model.generate_content(input_text)
    else:
        response=model.generate_content([input_text,image])
    return response.text

st.title('Invoice Extraxtion using Google Gemini')

st.write('Upload an invoice (image or PDF) and ask questions about the extraxted content.')

input_text=st.text_input('Enter your query.')

upload_file=st.file_uploader('Upload an invoice (Image/PDf)',type=['jpg','jpeg','pdf'])

image=None
text_from_pdf=None

if upload_file is not None:
    if upload_file.type in ['image/jpeg','image/jpg']:
        image=Image.open(upload_file)
        st.image(image,caption='uploaded Image',use_column_width=True)

    elif upload_file.type == 'application/pdf':
        with pdfplumber.open(io.BytesIO(upload_file.read())) as pdf:
            text_from_pdf=''
            for page in pdf.pages:
                extracted_text=page.extract_text()
                text_from_pdf+=extracted_text
            st.write('Extracted text from PDF')
            st.write(text_from_pdf)

input_prompt="you are an expert in understanding invoice. We will upload an invoice (Image or PDF) and you will answer questions base on the uploaded content."       

if st.button('Extract Information'):
    if image is not None :
        respons= get_gemini_response(input_prompt + input_text,image)
    elif text_from_pdf is not None:
        respons=get_gemini_response(input_prompt+ input_text + text_from_pdf)
    else :
        respons="Please upload a valid image or PDF file."
    st.write("Gemini's Response"
             )
    st.write(respons)
