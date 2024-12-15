import os
import streamlit as st
import pandas as pd
from groq import Groq

# Initialize Groq client with the API key from Streamlit secrets
client = Groq(api_key=st.secrets["groq"]["GROQ_API_KEY"])

# Streamlit UI
st.title("CampusGuideGPT - Study in Germany")

# Get user input for the query
query = st.text_input("Ask a question about studying in Germany:")

# Load the CSV data with questions and answers
df = pd.read_csv("https://raw.githubusercontent.com/mhd-faizzan/Groqtest/master/universities_data.csv")

# Function to search for a question and return the corresponding answer from CSV
def get_answer_from_csv(query, df):
    # Check if the query is in the 'Question' column (case insensitive)
    matches = df[df['Question'].str.contains(query, case=False, na=False)]
    if not matches.empty:
        # Return the first matching answer
        return matches.iloc[0]['Answer']
    return None

# Function to generate response from the model if no match is found
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

# Check if the query matches an entry in the CSV
if query:
    answer = get_answer_from_csv(query, df)
    if answer:
        st.write("Answer from CSV:", answer)
    else:
        response = generate_response(query)
        st.write("Response from LLM:", response)
