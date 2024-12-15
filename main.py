import streamlit as st
from groq import Groq
from fuzzywuzzy import fuzz

# Predefined Questions and Answers
qa_data = [
    {
        "question": "What is the focus of the Technology and Innovation Management (TIM) program?",
        "answer": "The Technology and Innovation Management (TIM) program focuses on equipping students with the skills to analyze innovation trends, identify future business opportunities, and make informed decisions about managing innovation. It combines engineering, IT, and business competences to address challenges in digitalization, automation, and business process integration. The program emphasizes applied science and recent trends in digital transformation, preparing students to take on managerial and technical responsibilities."
    },
    {
        "question": "How does the TIM program prepare students for careers in innovation and technology?",
        "answer": "The program prepares students by teaching them to analyze current innovation trends, systematically implement innovation processes, link automation and digitalization solutions with business processes, plan and advocate for projects, and take on management roles in technology-driven environments."
    },
    {
        "question": "What is the teaching language of the TIM program?",
        "answer": "The program is taught entirely in English, with German recommended for better integration into the local environment."
    },
    {
        "question": "Are there any fees for the program?",
        "answer": "There are no tuition fees for this program. However, students are required to pay a semester contribution of 118 EUR, which includes free regional public transportation and a contribution to the student body."
    },
    {
        "question": "What are the admission requirements for the TIM program?",
        "answer": "To qualify for admission: A first university degree with a GPA of 2.5 or higher on the German scale. A degree with at least 180 ECTS credit points for Regular Track or 210 ECTS credit points for Fast Track. A relevant degree in industrial engineering, business informatics, technical management, or a related engineering subject. A minimum of 10 weeks of professional experience related to the previous degree’s subject area. Proof of English proficiency at a B2 level. If the prior degree was conducted in English, no separate language certificate is required."
    },
    {
        "question": "What are the deadlines for applications?",
        "answer": "For applicants with a foreign academic degree (via uni-assist.de): Winter Semester: June 15th, Summer Semester: December 15th. For applicants with a German academic degree (via hs-harz.de): Winter Semester: July 15th, Summer Semester: January 15th."
    },
    {
        "question": "What is the difference between the Regular Track and Fast Track?",
        "answer": "Regular Track (4 semesters): Open to candidates with a 180 ECTS credit degree. Includes an adjustment semester with foundational courses. Fast Track (3 semesters): Open to candidates with a 210 ECTS credit degree. Does not include the adjustment semester."
    },
    {
        "question": "What career opportunities does the TIM program offer?",
        "answer": "Graduates are prepared to support businesses in implementing innovative technologies, manage digitalization processes, pursue managerial roles, and engage in research or doctoral studies."
    },
    {
        "question": "Can students opt for internships or an exchange semester during the TIM program?",
        "answer": "Yes, students can choose to do an internship or an exchange semester abroad. However, this is optional and is recommended only during the fourth semester."
    },
    {
        "question": "What core subjects are taught in the TIM program?",
        "answer": "Core subjects include Strategic Innovation Management, Operations Research, Agile Requirements Engineering, Digital Business Models, Big Data and Geoinformation, Technology Assessment, and more."
    },
    {
        "question": "What types of assessments are used in the TIM program?",
        "answer": "Students are evaluated through project work reports, presentations, written and oral examinations, term papers, software drafts, Master Thesis, and colloquium."
    },
    {
        "question": "What options are available for online study?",
        "answer": "Online study is available only for first-semester students, allowing flexibility for those unable to attend in person initially."
    },
    {
        "question": "How does the TIM program incorporate digitalization and Industry 4.0 concepts?",
        "answer": "The program emphasizes digital transformation strategies, integration of digital tools in business processes, and emerging trends like Mixed Reality and Smart Buildings."
    },
    {
        "question": "What is the purpose of the adjustment semester in the Regular Track?",
        "answer": "The adjustment semester bridges gaps in prior education for students with 180 ECTS credits. It covers foundational topics like Environment, Health, and Safety, Research Fields in Computer Science, and Engineering Projects."
    },
    {
        "question": "Where can students find more details about admission requirements and documents?",
        "answer": "Detailed information about admission requirements and required documents can be found at https://www.hs-harz.de/en/study/degree-students/international-applicants/master/."
    }
]

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
