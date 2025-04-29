import streamlit as st
import cv2
import pytesseract
from pdf2image import convert_from_path
import os
from deep_translator import GoogleTranslator
from fpdf import FPDF
import tempfile
import sys

# Set page config
st.set_page_config(
    page_title="OCR & Translation",
    page_icon="📝",
    layout="wide"
)

# Add home button
if st.button("🏠 Home", key="home_ocr"):
    st.session_state.page = "home"
    st.switch_page("main.py")


import cv2
import pytesseract
from pdf2image import convert_from_path
from deep_translator import GoogleTranslator
from fpdf import FPDF




# Function to split text into chunks
def split_text_into_chunks(text, max_chars=4000):
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 1 > max_chars:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = paragraph
        else:
            if current_chunk:
                current_chunk += "\n" + paragraph
            else:
                current_chunk = paragraph
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

# Function to translate long text
def translate_long_text(text, target_lang):
    chunks = split_text_into_chunks(text)
    translated_chunks = []
    
    for chunk in chunks:
        try:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(chunk)
            translated_chunks.append(translated)
        except Exception as e:
            st.warning(f"Error translating chunk: {str(e)}")
            translated_chunks.append(chunk)
    
    return "\n".join(translated_chunks)

# Function to create PDF
def create_pdf(text, output_path):
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_margins(20, 20, 20)  # left, top, right margins
        
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Translated Text', 0, 1, 'C')
            self.ln(10)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Set font for content
    pdf.set_font('Arial', '', 12)
    
    # Split text into paragraphs and add to PDF
    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        if paragraph.strip():  # Only add non-empty paragraphs
            # Convert paragraph to ASCII if it contains non-ASCII characters
            try:
                paragraph.encode('ascii')
                pdf.multi_cell(170, 10, paragraph)
            except UnicodeEncodeError:
                ascii_paragraph = paragraph.encode('ascii', 'ignore').decode('ascii')
                pdf.multi_cell(170, 10, ascii_paragraph)
            pdf.ln(5)  
    
    pdf.output(output_path)

# Main app
st.title("📝 OCR & Translation")
st.markdown("""
This app allows you to:
- Extract text from images
- Extract text from PDFs
- Translate the extracted text to multiple languages
- Download the translated text as PDF
""")

# File upload section
st.header("Upload File")
file_type = st.radio("Select file type:", ["Image", "PDF"])
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        if file_type == "Image":
            # Save the uploaded image
            image_path = os.path.join(temp_dir, "temp_image.png")
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Read and process image
            img = cv2.imread(image_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Display the image
            st.image(img_rgb, caption="Uploaded Image", use_column_width=True)
            
            # Extract text
            text = pytesseract.image_to_string(img_rgb, lang='eng+hin+deu+ara+spa+chi_sim')
            
        else:  # PDF
            
                # Save the uploaded PDF
                pdf_path = os.path.join(temp_dir, "temp.pdf")
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Convert PDF to images and extract text
                images = convert_from_path(pdf_path)
                text = ""
                for i, img in enumerate(images):
                    image_path = os.path.join(temp_dir, f"page_{i + 1}.png")
                    img.save(image_path, 'PNG')
                    text += f"\n--- Page {i + 1} ---\n"
                    text += pytesseract.image_to_string(image_path)
                
                # Display first page of PDF
                st.image(images[0], caption="First Page of PDF", use_column_width=True)
            

        # Display extracted text
        st.header("Extracted Text")
        st.text_area("", text, height=200)

        # Translation section
        st.header("Translation")
        language_options = {
            "1": "english",
            "2": "hindi",
            "3": "german",
            "4": "arabic",
            "5": "french",
            "6": "spanish",
            "7": "chinese (simplified)"
        }

        # Show language options
        st.write("Choose your preferred translation language:")
        for key, value in language_options.items():
            st.write(f"{key}. {value.title()}")

        # Language selection
        choice = st.selectbox(
            "Select target language:",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x].title()
        )

        if st.button("Translate"):
            target_lang = language_options[choice]
            with st.spinner("Translating..."):
                translated = translate_long_text(text, target_lang)
            
            # Display translated text
            st.header(f"Translated Text ({target_lang.title()})")
            st.text_area("", translated, height=200)

            # Create PDF with translated text
            pdf_path = os.path.join(temp_dir, "translated.pdf")
            create_pdf(translated, pdf_path)
            
            # Provide download button
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download Translated PDF",
                    data=f,
                    file_name="translated.pdf",
                    mime="application/pdf"
                ) 