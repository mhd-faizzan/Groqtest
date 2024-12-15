import streamlit as st
from groq import Groq
from fuzzywuzzy import fuzz

# Predefined Questions and Answers
predefined_qa = {
    "what are the requirements for studying in germany?": "You need a valid passport, proof of university admission, sufficient financial resources, and health insurance.",
    "how can i apply for a german student visa?": "You need to gather all required documents, fill out the application form, and attend an interview at the German embassy or consulate.",
    "what is the language requirement for german universities?": "Most universities require proficiency in English (TOEFL/IELTS) or German (TestDaF/DSH) depending on the program.",
}

# Initialize Groq client with the API key from Streamlit secrets
client = Groq(api_key=st.secrets["groq"]["GROQ_API_KEY"])

# Function to get a predefined answer
def get_predefined_answer(query):
    best_match = None
    highest_score = 0

    # Match query with predefined questions
    for question, answer in predefined_qa.items():
        score = fuzz.partial_ratio(query.lower(), question.lower())
        if score > highest_score:
            highest_score = score
            best_match = answer

    # Set a threshold to determine if a match is good enough
    if highest_score > 70:  # Adjust the threshold as needed
        return best_match
    return None

# Function to generate response from the LLM
def get_llm_response(query):
    try:
        # Create chat completion request to Groq API using llama3-70b-8192 model
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model="llama3-70b-8192",  # Ensure you are using the correct model name
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"(Unable to get LLM response: {str(e)})"

# Streamlit UI
st.title("CampusGuideGPT")
st.write("Your guide to studying in Germany! Ask your questions below.")

# Get user input for the query
query = st.text_input("Ask a question about studying in Germany:")

if query:
    # First try to get an answer from predefined QA
    predefined_answer = get_predefined_answer(query)

    # Get LLM response for additional information
    llm_response = get_llm_response(query)

    # Combine answers
    if predefined_answer:
        response = predefined_answer
        if llm_response:
            response += f"\n\nAdditional Information: {llm_response}"
    else:
        response = llm_response or "Sorry, I couldn't find an answer to your question."

    # Display the response
    st.write(response)
