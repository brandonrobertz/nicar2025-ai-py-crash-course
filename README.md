# NICAR 2025 AI Python Crash Course

Code and resources for the NICAR 2025 AI starter pack Python workshop

This demonstrates using LLM and Hugging Face models for basic journalism tasks.

Quickstart: `./bootstrap.sh`

We'll go through all of the steps one by one below.

## 01: Set up Ollama

Instructions are found here: [https://ollama.com/download/mac](https://ollama.com/download/mac)

You'll need to extract the zip and run the `ollama` command found inside. It will prompt you for access, which you'll need to grant. If it asks to install the shell command, do it.

Once you set this up, test you can run the `ollama` command on your command line. You should see something like:

```
$ ollama
Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model from a Modelfile
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information

Use "ollama [command] --help" for more information about a command.
```

## 02: Set up Python

Set up a virtual environment, install dependencies.

Run these steps:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python load_ai.py
```

This will take a minute, as it will download the model and run an example prompt.

After a few minutes, make sure you get a response better than this:

```
The NICAR (News Investigators and Reporters) Conference is an annual gathering of investigative journalists, researchers, and media professionals focused on investigative reporting, data journalism, and storytelling techniques. It's organized by the Center for Investigative Reporting at the University of California, Berkeley.
```

## 03: Set up file loading and prompt

Make sure the file you want to load is in the repo directory. Two files have been provided as an example that you can use.

I have a function provided that can load the data.

Our prompt is going to extract basic information from our PDF text file (`police_files_extract_json.basic.txt`).

```
python run_extraction.py
```

This will parse the files and spit out JSON results from each.

## 04: Try a classification prompt

We can also use an LLM to categorize information. We have a prompt that will do that for us as well (`police_files_extract_json.classify.txt`)

```
python run_extraction.py data/IAPRO_UOF_2010-2020_Pgs.001-350_Requestor_Copy.json prompts/police_files_extract_json.classify.txt
```

We'll get back results like:

```
Response: ```json
{
  "Force Type": "Detain",
  "Result type": "Wrong Person",
  "Accident": false
}
```

## 05: Meet Hugging Face

Ollama is good for a lot of things, but if you need something more specialized then you might need to turn to [Hugging Face](https://huggingface.co/models).

Hugging Face houses models for all kinds of tasks, and also provides a library that makes it easy to load and run them.

We have a basic code example that runs a NER model on some data. It will attempt to extract the names of people and organizations from the text.

This example will extract the people named inside:

```
python run_entity_extract.py data/example_entities.txt PER
```

This works well but what if it's uncased? Can we get people back?

```
python run_entity_extract.py data/example_entities.lower.txt PER
```

We can try another model.

```
dslim/bert-base-NER-uncased
```


## 06: Try against the folder of files

```
python run_entity_extract.py data/police_files/ ORG
```

We can take any NER model off here and use it directly. Most models have a piece of code in the README we can use, too. Copy pasta that and run it. Test out a bunch of models.

