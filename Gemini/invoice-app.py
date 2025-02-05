import os
import streamlit as st

st.title("API Key Viewer")

api_key = os.getenv("API_KEY")  # Fetch the API key from environment variables

if api_key:
    st.write(f"Last 4 characters of API key: `{api_key[-4:]}`")
else:
    st.error("API_KEY is not set in the environment.")
