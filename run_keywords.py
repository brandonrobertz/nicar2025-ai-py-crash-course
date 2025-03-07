import sys

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from transformers import logging


# Suppress the BERT unused weights warning
logging.set_verbosity_error()


model_name = "dslim/bert-base-NER"
texts = [
    "Artificial intelligence at the DOE is transforming healthcare and education.",
    "The Department of Education is cooperating with ICE to identify and deport students with immigrant parents, regardless of legality."
]

tokenizer = AutoTokenizer.from_pretrained(
    model_name, clean_up_tokenization_spaces=True,
)
model = AutoModelForTokenClassification.from_pretrained(model_name)
nlp = pipeline("ner", model=model, tokenizer=tokenizer)


def extract_organizations(entities):
    """
    Extract organization names from Hugging Face NER model output.

    Args:
        entities (list): List of entity dictionaries with 'entity', 'word', etc.

    Returns:
        list: List of organization names with proper formatting
    """
    organizations = []
    current_org = []

    for entity in entities:
        # Skip if not an organization entity
        if entity['entity'] not in ['B-ORG', 'I-ORG']:
            continue

        # If we encounter a B-ORG and already have an org in progress, save it
        if entity['entity'] == 'B-ORG' and current_org:
            organizations.append(" ".join(current_org))
            current_org = []

        # Clean up tokenization artifacts (like ##)
        word = entity['word']
        if word.startswith('##'):
            # Handle subword tokens that start with ##
            if current_org:
                # Append to the last word without space
                current_org[-1] += word[2:]
            else:
                # Unlikely case, but handle it
                current_org.append(word[2:])
        else:
            current_org.append(word)

    # Add the last organization if there's one in progress
    if current_org:
        organizations.append(" ".join(current_org))

    return organizations


def get_keywords(text):
    ner_results = nlp(text)
    print("ner_results", ner_results)
    if not ner_results:
        return
    keywords = [kw for kw in extract_organizations(ner_results)]
    print("Keywords:", keywords, file=sys.stderr)
    return keywords

if __name__ == "__main__":
    for txt in texts:
        kwds = get_keywords(txt)
        print("Text:", txt)
        print("Keywords:", kwds)
