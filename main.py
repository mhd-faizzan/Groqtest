import os
import streamlit as st
from groq import Groq

# Initialize Groq client with the API key from Streamlit secrets
client = Groq(api_key=st.secrets["groq"]["GROQ_API_KEY"])

# Streamlit UI
st.title("CampusGuideGPT - Study in Germany")

# Get user input for the query
query = st.text_input("Ask a question about studying in Germany:")

# Predefined questions and answers
qa_data = [
    {"question": "What is the capital of Germany?", "answer": "The capital of Germany is Berlin."},
    {"question": "What is the duration of a master's degree in Germany?", "answer": "A master's degree typically takes 2 years in Germany."},
    {"question": "What are the tuition fees for universities in Germany?", "answer": "Most public universities in Germany do not charge tuition fees for international students, except for a semester fee."},
    {"question": "Is learning German necessary for studying in Germany?", "answer": "While many programs are in English, learning German can be very beneficial for living and working in Germany."},
]

# Function to search for a question and return the corresponding answer from predefined data
def get_answer_from_qa(query):
    for item in qa_data:
        if query.lower() in item["question"].lower():
            return item["answer"]
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

# Check if the query matches an entry in the predefined data
if query:
    answer = get_answer_from_qa(query)
    if answer:
        st.write("Answer from predefined data:", answer)
    else:
        response = generate_response(query)
        st.write("Response from LLM:", response)
