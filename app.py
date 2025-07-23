import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv
import pdfplumber

# Load OpenAI API Key from .env
load_dotenv("openai-key.env")
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.warning("OpenAI API key not found. Please set it in openai-key.env.")

# Streamlit App Title
st.title("Tax Document Analyzer (PDF Upload)")
st.markdown("""
    Upload your W-2 and 1040 forms in PDF format to receive a tax breakdown and explanation.
""")

# File upload for W-2 and 1040 PDFs
w2_pdf = st.file_uploader("Upload W-2 PDF file", type=["pdf"])
form_1040_pdf = st.file_uploader("Upload 1040 PDF file", type=["pdf"])

# Function to query OpenAI GPT
def query_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use your fine-tuned model ID here if available
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response['choices'][0]['message']['content'].strip()

# Function to extract data from PDF (W-2 example)
def extract_w2_data(pdf):
    with pdfplumber.open(pdf) as pdf_doc:
        first_page = pdf_doc.pages[0]
        text = first_page.extract_text()
        
    # Simple text extraction for demonstration (you can refine this)
    wages = None
    federal_tax = None
    state_tax = None

    for line in text.split("\n"):
        if "Wages" in line:
            wages = line.split()[-1]  # Extracting last value (e.g., $92,000)
        if "Federal income tax withheld" in line:
            federal_tax = line.split()[-1]
        if "State income tax" in line:
            state_tax = line.split()[-1]

    return {
        "wages": wages,
        "federal_tax": federal_tax,
        "state_tax": state_tax
    }

# Function to extract data from PDF (1040 example)
def extract_1040_data(pdf):
    with pdfplumber.open(pdf) as pdf_doc:
        first_page = pdf_doc.pages[0]
        text = first_page.extract_text()

    # Extract key data from the form (you can refine this further)
    taxable_income = None
    refund = None

    for line in text.split("\n"):
        if "Taxable income" in line:
            taxable_income = line.split()[-1]  # Extracting last value
        if "Refund" in line:
            refund = line.split()[-1]

    return {
        "taxable_income": taxable_income,
        "refund": refund
    }

# Function to create a detailed and improved prompt for GPT
def create_refined_prompt(w2_data, f1040_data):
    return (
        f"You are a helpful assistant who explains tax documents in a simple and clear manner. "
        f"Below are the extracted W-2 and 1040 forms for a taxpayer. Your task is to:\n\n"
        
        f"1. Summarize the user’s earnings (from both W-2 and 1040), including total wages, income, and any adjustments.\n"
        f"2. Explain how much federal tax was withheld from the W-2 and compare it with the calculated tax due from the 1040.\n"
        f"3. Identify the taxable income (from 1040) and any potential refund or amount owed.\n"
        f"4. If the taxpayer is owed a refund, explain why and how much. If the taxpayer owes taxes, explain why and how much.\n"
        f"5. Include any additional relevant notes, such as eligibility for tax credits, standard deductions, or potential errors to watch out for.\n\n"
        
        f"Please ensure your explanation is clear, and guide the user through their tax situation step-by-step. "
        f"Make sure to avoid jargon, and explain terms in simple language when necessary.\n\n"
        
        f"W-2 Data:\n{json.dumps(w2_data, indent=2)}\n\n"
        f"1040 Data:\n{json.dumps(f1040_data, indent=2)}"
    )

# Function to process the uploaded files
def process_files(w2_pdf, form_1040_pdf):
    # Extract data from W-2 PDF
    w2_data = extract_w2_data(w2_pdf)
    
    # Extract data from 1040 PDF
    form_1040_data = extract_1040_data(form_1040_pdf)
    
    # Create the refined prompt
    prompt = create_refined_prompt(w2_data, form_1040_data)

    # Query GPT for explanation
    explanation = query_gpt(prompt)
    return explanation

# If both PDFs are uploaded, process them
if w2_pdf and form_1040_pdf:
    with st.spinner('Processing files...'):
        explanation = process_files(w2_pdf, form_1040_pdf)
    
    # Display the explanation
    st.subheader("Tax Explanation")
    st.write(explanation)

# Optionally, handle PDF extraction errors or incomplete data
if not w2_pdf or not form_1040_pdf:
    st.warning("Please upload both W-2 and 1040 PDF files to get the explanation.")