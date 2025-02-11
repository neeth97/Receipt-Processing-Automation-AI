from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import openai

# Load environment variables
load_dotenv()

# Configure OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get AI response
def get_openai_response(image):
    prompt = """
    You are an expert in understanding invoices.
    You will receive an invoice image and need to extract the following details:
    1) Identify where the invoice is from (company name).
    2) Identify and print the total amount spent.
    3) Determine the nature of the bill (Restaurant, Travel Expense, or Accommodation). Could you identify the category? Could you not explain the reasoning?
    """
    response = openai.Image.create(
        prompt=prompt,
        images=[{"image": image[0]}]
    )
    return response['data'][0]['text']

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    return None

# Streamlit App
st.set_page_config(page_title="Invoice Analyzer")
st.header(f"Invoice Analysis with OpenAI")

uploaded_file = st.file_uploader("Upload an invoice image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice.", width=300)
    
    image_data = input_image_setup(uploaded_file)
    if image_data:
        response = get_openai_response(image_data)
        st.subheader("Extracted Invoice Details:")
        st.write(response)
