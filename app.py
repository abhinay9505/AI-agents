import streamlit as st
import pandas as pd
import json
from langchain_experimental.agents import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType

# Function to load and parse uploaded file
def load_file(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        if file_type in ['csv', 'txt']:
            return pd.read_csv(uploaded_file)
        else:
            st.error("Unsupported file type.")
            return None
    return None
import tempfile
import os

# Function to create agent for answering questions about CSV data
def create_agent(data):
    if data is not None:
        # Use tempfile to create a temporary file path
        with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.csv') as temp_file:
            temp_file_path = temp_file.name
            # Save the uploaded data as a CSV in the temporary file
            data.to_csv(temp_file_path, index=False)
   # Create LangChain Agent with Gemini model
        agent = create_csv_agent(
            ChatGoogleGenerativeAI(
                google_api_key="AIzaSyDoj55tMl3TGuOTqTwsxKHZY6-sF-n6hCs", 
                model="gemini-1.5-pro-latest"
            ),
            temp_file_path,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            allow_dangerous_code=True  # Enable this functionality
        )
        return agent
    else:
        return None

# Streamlit App
st.title("AI Agent for Data Analysis")

st.sidebar.header("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx", "json", "txt"])

data = load_file(uploaded_file)
if data is not None:
    st.write("### Uploaded Data")
    st.dataframe(data)

    st.write("### Ask a Question")
    question = st.text_input("Enter your question about the data:")

    # Create the LangChain agent
    agent = create_agent(data)

    if question and agent:
        response = agent.run(question)
        st.write("### Answer")
        st.write(response)
else:
    st.write("Please upload a file to get started.")