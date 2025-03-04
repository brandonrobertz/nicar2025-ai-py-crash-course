import sys

import ollama


QUESTION="What is the NICAR conference? Answer briefly."


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


response = ollama.chat(
    model=model,
    options={
        "temperature":0.0,
    },
    messages=[
        {
            'role': 'user',
            'content': QUESTION,
        },
    ],
)
print("Prompt:", QUESTION)
print("Response:", response.message.content)
