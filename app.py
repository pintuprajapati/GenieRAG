import streamlit as st
import requests
from io import BytesIO

API_URL = "http://localhost:8000"

st.set_page_config(page_title="GenieRAG - Q&A Agent", layout="centered")

st.title("GenieRAG")

# --- Section 1: Upload PDF ---
st.header("1️⃣ Upload PDF File")

with st.form("upload_form"):
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    upload_submit = st.form_submit_button("Upload and Process")

if upload_submit and uploaded_file:
    with st.spinner("Processing PDF..."):
        files = {"file": (uploaded_file.name, BytesIO(uploaded_file.read()), "application/pdf")}
        response = requests.post(f"{API_URL}/ai/documents/ingest", files=files)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error("Something went wrong with the upload.")

# --- Section 2: Ask a Question ---
st.header("2️⃣ Ask a Question")

with st.form("question_form"):
    user_query = st.text_input("Ask something interesting")
    llm_choice = st.selectbox("Choose LLM", options=["openai", "claude"])
    query_submit = st.form_submit_button("Ask")

if query_submit and user_query:
    with st.spinner("Fetching answer..."):
        params = {
            "query": user_query,
            "llm": llm_choice
        }
        response = requests.get(f"{API_URL}/ai/query", params=params)

        if response.status_code == 200:
            data = response.json()['data']
            st.success(data.get('llm_response'))
        else:
            st.error("Failed to fetch answer.")
