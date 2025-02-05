import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("API key not found! Make sure it's defined in your .env file.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Helper function for calling the Generative AI model
def gemini_response(input_query, image_data, prompt):
    response = model.generate_content([input_query, image_data[0], prompt])
    return response.text

# Helper function to process uploaded image
def extract_image_data(uploaded_file):
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts

# Streamlit app setup
st.set_page_config(page_title="Bill Extractor Application")
st.header("Bill Extractor Application")

# Initialize session state for storing extracted data and chat history
if "image_data" not in st.session_state:
    st.session_state.image_data = None  # Store image data extracted from OpenAI
if "extracted_response" not in st.session_state:
    st.session_state.extracted_response = None  # Store extracted data response
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Store user questions and AI responses

# Default input for image extraction
default_prompt = "This is an image of an invoice or bill. Extract its data in a table format."
uploaded_file = st.file_uploader("Choose an image:", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image!!!", use_container_width=True)

    # Extract image data and call OpenAI only once
    if st.session_state.image_data is None:
        st.session_state.image_data = extract_image_data(uploaded_file)
        with st.spinner("Extracting data from the image..."):
            extracted_response = gemini_response(default_prompt, st.session_state.image_data, "Extract information as a table.")
            st.session_state.extracted_response = extracted_response  # Store the response
            # st.session_state.chat_history.append({"role": "assistant", "content": extracted_response})

    # Display the extracted data
    st.subheader("Extracted Information:")
    st.write(st.session_state.extracted_response)

# Chat loop interface for asking follow-up questions
st.subheader("Ask Questions Based on Extracted Data")
user_input = st.text_input("Question:", key="user_input")
if st.button("Get Answer"):
    if user_input:
        # Append user input to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Generate a response using the extracted data
        with st.spinner("Generating response..."):
            response = gemini_response("Answer based on extracted data.", st.session_state.image_data, user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

        # Display chat history
        st.subheader("Chat History")
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            elif message["role"] == "assistant":
                st.markdown(f"**AI:** {message['content']}")
                st.write("-----------------------------------")
