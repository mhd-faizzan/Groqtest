import os
import streamlit as st
import pandas as pd
import requests
from groq import Groq

# Initialize Groq client with the API key from Streamlit secrets
client = Groq(api_key=st.secrets["groq"]["GROQ_API_KEY"])

# Load the CSV from GitHub
csv_url = "https://raw.githubusercontent.com/mhd-faizzan/Groqtest/master/universities_data.csv"  # Updated URL
df_universities = pd.read_csv(csv_url)

# Predefined content dictionary (optional for static data)
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

# Function to check if the question exists in the CSV
def get_answer_from_csv(query):
    # Check if the query matches any question in the CSV
    matching_row = df_universities[df_universities['Question'].str.contains(query, case=False, na=False)]
    if not matching_row.empty:
        return matching_row.iloc[0]['Answer']
    return None  # Return None if no match is found

# Function to generate response from the model
def generate_response(query):
    try:
        # Retrieve answer from the CSV if available
        csv_answer = get_answer_from_csv(query)
        
        if csv_answer:
            # If the answer is found in the CSV, return it directly
            return csv_answer
        else:
            # If no match is found in CSV, use the predefined content or call the Groq model
            predefined_response = get_predefined_content(query)
            
            if predefined_response:
                # If predefined content is found, return it
                input_text = f"Based on this information: {predefined_response}\nAnswer the user's question: {query}"
            else:
                # Otherwise, fetch dynamic data using Groq LLM
                input_text = f"Answer the user's question: {query}"

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
    
    # Fetch the response from the model or CSV
    response = generate_response(query)
    
    # Display the response in a styled way
    st.markdown(f'<p class="response-text">Response: {response}</p>', unsafe_allow_html=True)
