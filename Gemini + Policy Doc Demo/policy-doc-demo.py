from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import docx

# Load environment variables
load_dotenv()

# Configure API Key
google_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=google_api_key)

# Function to extract rules from the policy document
def extract_policy_rules(doc_path):
    try:
        doc = docx.Document(doc_path)
        rules = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return rules
    except Exception as e:
        return f"Error reading policy document: {e}"

# Function to get AI response
def get_gemini_response(image, policy_rules):
    prompt = f"""
    You are an expert in understanding invoices and verifying compliance with company policies.
    You will receive an invoice image and the company’s policy document.
    Extract the following details from the invoice:
    
    1) Identify where the invoice is from (company name).
    2) Identify and print the total amount spent.
    3) Determine the nature of the bill (Restaurant, Travel Expense, or Accommodation).
    4) Approve or reject the expense based on the following policy rules:
    
    {policy_rules}
    
    Provide a clear yes/no response for approval and mention any violations.
    """
    
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content([prompt, image[0]])
    return response.text

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    return None

# Streamlit App
st.set_page_config(page_title="Invoice Analyzer")
st.header("Invoice Analysis with Gemini AI")

uploaded_file = st.file_uploader("Upload an invoice image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice.", width=300)
    
    image_data = input_image_setup(uploaded_file)
    policy_rules = extract_policy_rules("ExpenseNow Sample Expense Policy.docx")
    
    if image_data and policy_rules:
        response = get_gemini_response(image_data, policy_rules)
        st.subheader("Extracted Invoice Details & Approval Status:")
        st.write(response)
