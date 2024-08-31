import streamlit as st
import PyPDF2
import anthropic
import os
import fitz  # PyMuPDF
from io import BytesIO

# Set up Anthropic API key
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
client = anthropic.Anthropic(api_key=anthropic_api_key)

def summarize_page(page_content):
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="You are an AI assistant specializing in summarizing academic content. Provide concise summaries in Thai.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Please summarize the following page content in Thai:\n\n{page_content}"
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def get_pdf_page_as_image(pdf_content, page_number):
    pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
    page = pdf_document.load_page(page_number)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img_bytes = pix.tobytes("png")
    return img_bytes

@st.cache_data
def get_pdf_summary(_pdf_content, page_number):
    pdf_reader = PyPDF2.PdfReader(BytesIO(_pdf_content))
    page_content = pdf_reader.pages[page_number].extract_text()
    return summarize_page(page_content)

def main():
    st.set_page_config(layout="wide")
    st.title("PDF Lecture AI Assistant")

    if "summaries" not in st.session_state:
        st.session_state.summaries = {}
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1
    if "user_question" not in st.session_state:
        st.session_state.user_question = ""

    uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

    if uploaded_file is not None:
        pdf_content = uploaded_file.read()
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
        num_pages = len(pdf_reader.pages)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("PDF Content")
            page_number = st.number_input("Select page", min_value=1, max_value=num_pages, value=st.session_state.current_page)
            
            # Check if page has changed
            if page_number != st.session_state.current_page:
                st.session_state.current_page = page_number
                st.session_state.user_question = ""  # Reset the question
            
            # Display PDF page as image
            img_bytes = get_pdf_page_as_image(pdf_content, page_number - 1)
            st.image(img_bytes, use_column_width=True)

        with col2:
            st.subheader("AI Assistant")
            
            # Display summary
            summary_key = f"summary_{page_number-1}"
            if summary_key not in st.session_state:
                with st.spinner("Generating summary..."):
                    page_content = pdf_reader.pages[page_number - 1].extract_text()
                    summary = summarize_page(page_content)
                    st.session_state[summary_key] = summary
            
            st.write("Summary:")
            st.write(st.session_state[summary_key])

            # Chat interface
            user_question = st.text_input("Ask a question about this page:", value=st.session_state.user_question)
            
            # Update the stored question
            st.session_state.user_question = user_question

            if user_question:
                with st.spinner("Generating answer..."):
                    page_content = pdf_reader.pages[page_number - 1].extract_text()
                    message = client.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=1000,
                        temperature=0,
                        system="You are an AI assistant specializing in answering questions about academic content. Provide answers in Thai.",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Based on the following page content and summary, please answer the user's question in Thai:\n\nPage content: {page_content}\n\nSummary: {st.session_state[summary_key]}\n\nQuestion: {user_question}"
                                    }
                                ]
                            }
                        ]
                    )
                st.write("Answer:")
                st.write(message.content[0].text)

if __name__ == "__main__":
    main()