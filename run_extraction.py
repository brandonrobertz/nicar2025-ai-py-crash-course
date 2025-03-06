from datetime import datetime
import json
import sys

import ollama

from load_file import load_records


INFILE="data/IAPRO_UOF_2010-2020_Pgs.001-350_Requestor_Copy.json"
OUTFILE="output.{int(datetime.now().timestamp())}.json"
PROMPT="prompts/police_files_extract_json.basic.txt"


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
print("Using prompt template:\n-- BEGIN TEMPLATE --\n", prompt_base, "\n-- END TEMPLATE --")


extracted = []
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
    resp_text = response.message.content
    print("Response:", resp_text)

    extract = json.loads(resp_text.split(
        "```json", 1
    )[1].split("```", 1)[0])
    print("Extracted:", extracted)
    extracted.append(extract)


print("Writing", len(extracted), "records to", OUTFILE)
with open(OUTFILE, "w") as f:
    f.write(json.dumps(extracted, indent=2))
