import streamlit as st

# Set page config
st.set_page_config(
    page_title="Quiz App",
    page_icon="📚",
    layout="wide"
)

# Add home button
if st.button("🏠 Home", key="home_quiz"):
    st.session_state.page = "home"
    st.switch_page("main.py")


from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


# Load environment variables
load_dotenv()

# Initialize Groq
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.5)


# Define the prompt template
system_template = """You are an interactive and engaging language tutor. Your goal is to help the user learn a new language step by step with clear instruction, interactive exercises, quizzes, and assessments.

Start by briefly introducing the topic of the lesson.

Then follow this structure for every session:

1. Create a quiz to test and fun learning with 4 options to choose and provide answers also.
"""

user_template = "i know {fr} and i want to learn {to} and the level is {level} and number of questions is {questions}."

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", user_template)],
)

# Main app
st.title("📚 Language Learning Quiz")

with st.form("quiz_form"):
    col1, col2 = st.columns(2)
    with col1:
        fr = st.text_input("From Language")
        to = st.text_input("To Language")
    with col2:
        number = st.text_input("Number of Questions")
        level = st.text_input("Level of Questions")

    submitted = st.form_submit_button("Generate Quiz")
    
    if submitted:
        with st.spinner("Generating quiz..."):
            try:
                prompt = prompt_template.invoke({
                    "fr": fr,
                    "to": to,
                    "level": level,
                    "questions": number
                })
                response = llm.invoke(prompt)
                st.write(response.content)
            except Exception as e:
                st.error(f"Error generating quiz: {str(e)}") 
