from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import openai
import pytesseract

# Load environment variables
load_dotenv()

# Configure OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get OpenAI response
def get_openai_response(extracted_text):
    prompt = f"""
    You are an expert in understanding invoices.
    The text extracted from the invoice is as follows:
    {extracted_text}
    
    Please extract the following details:
    1) Identify where the invoice is from (company name).
    2) Identify and print the total amount spent.
    3) Determine the nature of the bill (Restaurant, Travel Expense, or Accommodation). Please identify the category only, without explaining the reasoning.
    """
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use any suitable engine
        prompt=prompt,
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    return None

# Streamlit App
st.set_page_config(page_title="Invoice Analyzer")
st.header(f"Invoice Analysis with OpenAI")

# Upload image
uploaded_file = st.file_uploader("Upload an invoice image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice.", width=300)
    
    # Extract text from image
    extracted_text = input_image_setup(uploaded_file)
    
    if extracted_text:
        st.subheader("Extracted Text from Invoice:")
        st.write(extracted_text)
        
        # Get OpenAI response based on extracted text
        response = get_openai_response(extracted_text)
        
        st.subheader("Extracted Invoice Details:")
        st.write(response)
