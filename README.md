# NICAR 2025 AI Python Crash Course

Code and resources for the NICAR 2025 AI starter pack Python workshop

## 01: Step One - Set up Ollama

Instructions are found here: [https://ollama.com/download/mac](https://ollama.com/download/mac)

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

## 02: Step Two - Set up Python

Set up a virtualenv, install dependencies.

Run these steps:

```
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python load_ai.py
```

This will take a minute, as it will download the model and run an example prompt.

After a few minutes, make sure you get a response better than this:

```
The NICAR (News Investigators and Reporters) Conference is an annual gathering of investigative journalists, researchers, and media professionals focused on investigative reporting, data journalism, and storytelling techniques. It's organized by the Center for Investigative Reporting at the University of California, Berkeley.
```

## 03: Step Three - Set up file loading and prompt

Make sure the file you want to load is in the repo directory. Two files have been provided as an example that you can use.

I have a function provided that can load the data.
