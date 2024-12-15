import os
import streamlit as st
from groq import Groq

# Initialize Groq client with the API key from Streamlit secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Streamlit UI
st.title("GenAI-based RAG Application")

# Get user input for the query
query = st.text_input("Ask a question about studying in Germany:")

# Function to generate response from the model
def generate_response(query):
    try:
        # Create chat completion request to Groq API using llama3-70b-8192 model
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model="llama3-70b-8192",  # Ensure you are using the correct model name
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error in prediction: {str(e)}"

if query:
    # Fetch the response from the model
    response = generate_response(query)
    st.write("Response:", response)