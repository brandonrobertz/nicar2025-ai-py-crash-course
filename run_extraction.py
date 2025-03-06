import json
import sys

import ollama

from load_file import load_records


INFILE="data/IAPRO_UOF_2010-2020_Pgs.001-350_Requestor_Copy.json"
PROMPT="prompts/police_files_extract_json.txt"


try:
    model = sys.argv[1]
except IndexError:
    model = 'llama3.2'

try:
    ollama.chat(model)
except ollama.ResponseError as e:
    if e.status_code == 404:
        print(f"Downloading model: {model}")
        ollama.pull(model)
    else:
        raise(e)

print("Loading prompt", PROMPT)
with open(PROMPT, "r") as f:
    prompt_base = f.read()
print("Using prompt template:", prompt_base)


records = load_records(INFILE, encoding='utf-8')
print("Loaded", len(records), "records")
for rec in records:
    prompt = prompt_base.format(rec=rec)
    response = ollama.chat(
        model=model,
        options={
            "temperature": 0.0,
        },
        messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ],
    )
    print("Response:", response.message.content)
