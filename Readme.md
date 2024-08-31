# 📚 PDF Lecture AI Assistant

This Streamlit application serves as an AI-powered assistant for PDF lectures. It allows users to upload PDF files, view pages, get Thai summaries, and ask questions about the content.

## ✨ Features

- 📄 PDF upload and page-by-page viewing
- 🇹🇭 Automatic Thai summarization of page content
- 🤖 AI-powered Q&A system in Thai
- 🖥️ User-friendly interface with side-by-side PDF view and AI assistant

## 🛠️ Requirements

- Python 3.7+
- Streamlit
- PyPDF2
- Anthropic API
- PyMuPDF (fitz)

## 🚀 Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your Anthropic API key as an environment variable: `ANTHROPIC_API_KEY`
4. Run the app: `streamlit run app.py`

## 📖 Usage

1. Upload a PDF file
2. Navigate through pages using the number input
3. View the Thai summary for each page
4. Ask questions about the content in the chat interface

## ℹ️ Note

This application uses the Anthropic API to generate summaries and answer questions. Ensure you have a valid API key and sufficient credits.