import os
import streamlit as st
from groq import Groq

# Initialize Groq client with the API key from Streamlit secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Streamlit UI
st.title("CampusGuideGPT")

# Add a description for a user-friendly interface
st.markdown("""
Welcome to CampusGuideGPT, your AI-powered assistant for all things related to studying abroad in Germany! 
Ask any question and get comprehensive answers powered by the latest language models.
""")

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

# If the user enters a query, generate and display the response
if query:
    # Fetch the response from the model
    response = generate_response(query)
    st.write("Response:", response)

    # Optionally, add some styling to make the response more visually appealing
    st.markdown(f"""
    <div style="background-color: #f0f0f5; padding: 10px; border-radius: 5px;">
        <b>Answer:</b> {response}
    </div>
    """, unsafe_allow_html=True)
