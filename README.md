# Tax Analyzer

## Overview

Tax Analyzer is a tool designed to generate plain-English explanations of a user's tax situation by analyzing W-2 and 1040 tax documents. It provides both a Streamlit web application for interactive PDF uploads and a script for generating fine-tuning data using synthetic JSON tax data and OpenAI's GPT models.

## Features
- **Streamlit Web App**: Upload W-2 and 1040 PDF files and receive a step-by-step tax explanation in plain English.
- **Fine-tuning Data Generation**: Loads paired W-2 and 1040 JSON tax data, generates prompts, and queries OpenAI's GPT-4 model to output explanations in JSONL format for fine-tuning.

## Project Structure

```
tax-analyzer/
├── app.py                        # Main entry point: Streamlit web app for PDF analysis
├── data/
│   ├── Download 1040 PDF.pdf
│   ├── Download W-2 PDF.pdf
│   ├── f1040.pdf
│   ├── fine_tuning_tax_explanations.jsonl
│   ├── fw2.pdf
│   └── synthetic_json/
│       └── linked/
│           ├── 1040_0.json ... 1040_99.json
│           └── w2_0.json ... w2_99.json
├── openai-key.env
├── scripts/
│   ├── generate_explanations_jsonl.py  # Script for generating fine-tuning data
│   └── generate_linked_tax_data.py
```

## Setup

1. **Clone the repository**

2. **Install dependencies**
   
   This project requires Python 3.7+ and the following packages:
   - streamlit
   - openai
   - python-dotenv
   - tqdm
   - pdfplumber

   Install them with:
   ```bash
   pip install streamlit openai python-dotenv tqdm pdfplumber
   ```

3. **Set up your OpenAI API key**
   
   - Create a file named `openai-key.env` in the project root with the following content:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Alternatively, you can directly set the API key in the code (not recommended for production).

## Usage

### 1. Run the Streamlit Web App (Main Entry Point)

The main entry point is `app.py`, which launches a web interface for uploading and analyzing tax PDFs.

```bash
streamlit run app.py
```

- Upload your W-2 and 1040 PDF files.
- The app will extract key data and provide a plain-English explanation of your tax situation, including earnings, tax withheld, taxable income, refund/amount owed, and more.

### 2. Generate Explanations JSONL (Fine-tuning Data)

Run the script to generate fine-tuning data from synthetic JSON files:

```bash
python scripts/generate_explanations_jsonl.py
```

This will process 100 pairs of W-2 and 1040 JSON files from `data/synthetic_json/linked/` and output the explanations to `data/fine_tuning_tax_explanations.jsonl`.

### Data
- **Input:** Paired W-2 and 1040 PDF files (for the app) or JSON files (for the script)
- **Output:** Tax explanations in the web app or in `data/fine_tuning_tax_explanations.jsonl`

## Notes
- The scripts currently use a hardcoded OpenAI API key for demonstration. For security, use environment variables instead.
- The explanations are generated using the GPT-4 model.

## License
Specify your license here. 