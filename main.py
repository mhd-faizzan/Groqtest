import os
import streamlit as st
from groq import Groq

# Initialize Groq client with the API key from Streamlit secrets
client = Groq(api_key=st.secrets["groq"]["GROQ_API_KEY"])

# Streamlit UI
st.title("CampusGuideGPT")

# Customize the prompt section
st.markdown("""
    <style>
        .prompt-text {
            font-size: 18px;
            font-weight: bold;
            color: #0077cc;
        }
        .response-text {
            font-size: 16px;
            color: #333;
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

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
    # Display the query in a styled way
    st.markdown(f'<p class="prompt-text">Your Question: {query}</p>', unsafe_allow_html=True)
    
    # Fetch the response from the model
    response = generate_response(query)
    
    # Display the response in a styled way
    st.markdown(f'<p class="response-text">Response: {response}</p>', unsafe_allow_html=True)
