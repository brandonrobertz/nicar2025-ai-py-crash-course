from datetime import datetime
import json
import sys

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from transformers import logging

from load_data import load_records


# Suppress the BERT unused weights warning
logging.set_verbosity_error()

try:
    INFILE=sys.argv[1]
except IndexError:
    INFILE="data/example_entities.txt"

# Entity type can be one of:
#   ORG - organization
#   PER - person name
#   LOC - location
try:
    ENTITY_TYPE = sys.argv[2]
except IndexError:
    ENTITY_TYPE="ORG"

try:
    MODEL = sys.argv[3]
except IndexError:
    MODEL = "dslim/distilbert-NER"

OUTFILE=f"output-orgs.{int(datetime.now().timestamp())}.json"


texts = load_records(INFILE)
print("Loaded", len(texts), "records")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL, clean_up_tokenization_spaces=True,
)
model = AutoModelForTokenClassification.from_pretrained(MODEL)
nlp = pipeline("ner", model=model, tokenizer=tokenizer,
               # This outputs grouped entities
               aggregation_strategy="simple")


def extract_entities(entities, etype="ORG"):
    """
    Extract full entity names (as strings) from Hugging Face NER model
    output, which outputs a data structure of standard NER tags.
    """
    entity_strings = []
    current_org = []

    for entity in entities:
        if entity.get("entity_group") != etype:
            continue
        entity_strings.append(entity["word"])

    final = []
    for e in entity_strings:
        if not e.startswith("##") or not final:
            final.append(e)
        else:
            final[-1] += e[2:]
    return final


def get_ents(text):
    ner_results = nlp(text)
    if not ner_results:
        return
    return [kw for kw in extract_entities(ner_results, etype=ENTITY_TYPE)]


out_data = []
for text in texts:
    ents = get_ents(text)
    if len(text) > 200:
        print("Text:", text[:200].replace("\n", " "), "... (truncated)")
    else:
        print("Text:", text)
    print("Entities:", ", ".join(ents) if ents else "none")
    out_data.append({
        "entities": ents,
        "text": text,
    })


print("Writing", len(out_data), "records to", OUTFILE)
with open(OUTFILE, "w") as f:
    f.write(json.dumps(out_data, indent=2))
