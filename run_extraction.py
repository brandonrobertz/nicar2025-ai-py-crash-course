from datetime import datetime
import json
import sys

import ollama

from load_data import load_records


try:
    INFILE=sys.argv[1]
except IndexError:
    INFILE="data/IAPRO_UOF_2010-2020_Pgs.001-350_Requestor_Copy.json"

try:
    PROMPT=sys.argv[2]
except IndexError:
    PROMPT="prompts/police_files_extract_json.basic.txt"

try:
    MODEL = sys.argv[3]
except IndexError:
    MODEL = 'llama3.2'

OUTFILE=f"output-extract.{int(datetime.now().timestamp())}.json"



try:
    ollama.chat(MODEL)
except ollama.ResponseError as e:
    if e.status_code == 404:
        print(f"Downloading model: {MODEL}")
        ollama.pull(MODEL)
    else:
        raise(e)


print("Loading prompt", PROMPT)
with open(PROMPT, "r") as f:
    prompt_base = f.read()
print("Using prompt template:\n-- BEGIN TEMPLATE --\n", prompt_base, "\n-- END TEMPLATE --")


extracted = []
records = load_records(INFILE, encoding='utf-8')
print("Loaded", len(records), "records")
for rec in records:
    prompt = prompt_base.format(rec=rec)
    response = ollama.chat(
        model=MODEL,
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
    resp_text = response.message.content
    print("Response:", resp_text)

    extracted_rec = json.loads(resp_text.split(
        "```json", 1
    )[-1].split("```", 1)[0])
    print("Extracted:", extracted_rec)
    if isinstance(extracted_rec, list):
        for er in extracted_rec:
            extracted.append(er)
    else:
        extracted.append(extracted_rec)


print("Writing", len(extracted), "records to", OUTFILE)
with open(OUTFILE, "w") as f:
    f.write(json.dumps(extracted, indent=2))
