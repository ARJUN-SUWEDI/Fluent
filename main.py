import streamlit as st

st.set_page_config(
    page_title="Fluent Now",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Multi-Feature Application")
st.markdown("""
Welcome to our multi-feature application! This app combines three powerful tools:

1. **OCR & Translation Tool** - Extract and translate text from images and PDFs
2. **Quiz App** - Test your knowledge with interactive quizzes
3. **Speech App** - Convert text to speech

Select a feature from the sidebar to get started!
""")

# Add some styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Create three columns for feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📝 OCR & Translation
    Extract text from images and PDFs, and translate it to multiple languages.
    """)
    if st.button("Go to OCR & Translation", key="ocr"):
        st.session_state.page = "ocr"

with col2:
    st.markdown("""
    ### 📚 Quiz App
    Test your knowledge with interactive quizzes on various topics.
    """)
    if st.button("Go to Quiz App", key="quiz"):
        st.session_state.page = "quiz"

with col3:
    st.markdown("""
    ### 🎤 Speech App
    Convert text to speech with multiple voice options.
    """)
    if st.button("Go to Speech App", key="speech"):
        st.session_state.page = "speech"

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Handle page navigation
if st.session_state.page == "ocr":
    st.switch_page("pages/ocr_app.py")
elif st.session_state.page == "quiz":
    st.switch_page("pages/quiz_app.py")
elif st.session_state.page == "speech":
    st.switch_page("pages/speech_app.py") 