import os
import streamlit as st
import pandas as pd
from groq import Groq

# Initialize Groq client with the API key from Streamlit secrets
client = Groq(api_key=st.secrets["groq"]["GROQ_API_KEY"])

# Load the CSV with university data (if you are using custom data as well)
df_universities = pd.read_csv('university_data.csv')

# Predefined content dictionary (for static information)
predefined_content = {
    "admission_process": "The admission process in Germany typically includes an online application, submission of required documents, and proof of language proficiency.",
    "living_in_germany": "Living in Germany is affordable compared to other European countries. Major cities like Berlin and Munich offer a high standard of living.",
    "visa_information": "To study in Germany, you need a student visa. Requirements include proof of acceptance from a German university and financial proof to cover living expenses."
}

# Streamlit UI
st.title("CampusGuideGPT")

# Customize the prompt section with CSS
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

# Function to retrieve predefined content based on query
def get_predefined_content(query):
    for topic, content in predefined_content.items():
        if topic.lower() in query.lower():
            return content
    return None  # Return None if no predefined content is found

# Function to generate response from the model
def generate_response(query):
    try:
        # Retrieve predefined content if available
        predefined_response = get_predefined_content(query)
        
        if predefined_response:
            # If predefined content is found, include it in the model input
            input_text = f"Based on this information: {predefined_response}\nAnswer the user's question: {query}"
        else:
            # Otherwise, retrieve dynamic data from the CSV (if any)
            custom_info = retrieve_custom_info(query, df_universities)
            input_text = f"Based on the following information: {custom_info}\nAnswer the user's question: {query}"
        
        # Create chat completion request to Groq API using llama3-70b-8192 model
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": input_text}],
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

