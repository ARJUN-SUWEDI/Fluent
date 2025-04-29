import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import os
import time

# Set page config
st.set_page_config(
    page_title="Speech App",
    page_icon="🎤",
    layout="wide"
)

# Add home button
if st.button("🏠 Home", key="home_speech"):
    st.session_state.page = "home"
    st.switch_page("main.py")

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Main app
st.title("🎤 Speech & Translation App")

# Language selection with full names
language_map = {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh"
}

target_language = st.selectbox(
    "Select target language:",
    list(language_map.keys())
)

# Create two columns for the two main features
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎙️ Speech to Text & Translation")
    
    # Initialize session state for recording
    if 'recording' not in st.session_state:
        st.session_state.recording = False
    
    # Recording button
    if not st.session_state.recording:
        if st.button("🎙️ Start Recording"):
            st.session_state.recording = True
            st.experimental_rerun()
    else:
        if st.button("⏹️ Stop Recording"):
            st.session_state.recording = False
            st.experimental_rerun()
    
    # Display recording status
    if st.session_state.recording:
        st.write("🎙️ Recording in progress... Speak into your microphone.")
        
        try:
            # Use the microphone as source
            with sr.Microphone() as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record audio
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                # Convert speech to text
                text = recognizer.recognize_google(audio)
                
                if text:
                    st.success("🎯 Recognized Text:")
                    st.write(text)
                    
                    # Translate the text
                    translated_text = GoogleTranslator(
                        source='auto',
                        target=language_map[target_language]
                    ).translate(text)
                    
                    st.success("🌐 Translated Text:")
                    st.write(translated_text)
                    
                    # Convert translated text to speech
                    tts = gTTS(
                        text=translated_text,
                        lang=language_map[target_language],
                        slow=False
                    )
                    
                    # Save and play the translated speech
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
                        tts.save(temp_audio.name)
                        st.audio(temp_audio.name)
        
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please try speaking more clearly.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

with col2:
    st.subheader("📝 Text to Speech")
    st.write("Enter text to translate and convert to speech:")
    
    # Text input for manual entry
    text_input = st.text_area("Type or paste your text here", height=100)
    
    if st.button("Translate Text"):
        if text_input:
            with st.spinner("Translating..."):
                try:
                    # Translate the text
                    translated_text = GoogleTranslator(
                        source='auto',
                        target=language_map[target_language]
                    ).translate(text_input)
                    
                    st.success("🌐 Translated Text:")
                    st.write(translated_text)
                    
                    # Convert translated text to speech
                    tts = gTTS(
                        text=translated_text,
                        lang=language_map[target_language],
                        slow=False
                    )
                    
                    # Save to a temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
                        tts.save(temp_audio.name)
                        st.audio(temp_audio.name)
                except Exception as e:
                    st.error(f"Translation error: {str(e)}")
        else:
            st.warning("Please enter some text to translate.")

# Instructions
st.markdown("""
### How to use:
1. Select your target language from the dropdown menu
2. Choose your preferred method:
   - **Speech to Text**: Click 'Start Recording' to begin recording your speech
   - **Text to Speech**: Type or paste text in the text area
3. The app will:
   - Convert your speech to text (if using audio)
   - Translate the text to your selected language
   - Convert the translation to speech
""") 