# OCR & Translation App

This Streamlit application allows you to extract text from images and PDFs, translate the text to multiple languages, and download the translated text as a PDF.

## Features

- Extract text from images (JPG, JPEG, PNG)
- Extract text from PDFs
- Support for multiple languages in OCR
- Translate extracted text to multiple languages
- Download translated text as PDF

## Prerequisites

- Python 3.7 or higher
- Tesseract OCR installed on your system

### Installing Tesseract OCR

#### Windows
1. Download the installer from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install and add the installation directory to your system PATH

#### Linux
```bash
sudo apt-get install tesseract-ocr
```

#### macOS
```bash
brew install tesseract
```

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the App

Run the following command in your terminal:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Usage

1. Select the type of file you want to process (Image or PDF)
2. Upload your file
3. The extracted text will be displayed
4. Choose your target language for translation
5. Click "Translate" to get the translated text
6. Download the translated text as PDF using the download button

## Supported Languages for Translation

- English
- Hindi
- German
- Arabic
- French
- Spanish
- Chinese (Simplified) 