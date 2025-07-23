import openai
import os
import json
from dotenv import load_dotenv
from tqdm import tqdm

# Load OpenAI Key
load_dotenv("../openai-key.env")
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set it in openai-key.env.")

DATA_DIR = "../data/synthetic_json/linked"
OUTPUT_JSONL = "../data/fine_tuning_tax_explanations.jsonl"

def load_pair(i):
    with open(os.path.join(DATA_DIR, f"w2_{i}.json")) as f1, open(os.path.join(DATA_DIR, f"1040_{i}.json")) as f2:
        w2 = json.load(f1)
        f1040 = json.load(f2)
    return w2, f1040

def create_prompt(w2, f1040):
    return (
        f"Here is the W-2 tax data:\n{json.dumps(w2, indent=2)}\n\n"
        f"Here is the 1040 tax return data:\n{json.dumps(f1040, indent=2)}\n\n"
        f"Explain the user's tax situation in plain English: include how much they earned, how much tax was withheld, "
        f"if they owe or will get a refund, and why."
    )

def query_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response['choices'][0]['message']['content'].strip()

def main():
    with open(OUTPUT_JSONL, "w") as outfile:
        for i in tqdm(range(100), desc="Generating explanations"):
            try:
                w2, f1040 = load_pair(i)
                prompt = create_prompt(w2, f1040)
                response = query_gpt(prompt)

                fine_tune_format = {
                    "messages": [
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": response}
                    ]
                }

                outfile.write(json.dumps(fine_tune_format) + "\n")

            except Exception as e:
                print(f"Error on record {i}: {e}")

if __name__ == "__main__":
    main()