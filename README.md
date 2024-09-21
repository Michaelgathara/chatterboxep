# chatterboxep

A python program that generates mp3 clips of AI podcasts. 

## Pre-Reqs:
OPENAI API KEY from https://playground.openai.com

ANTHROPIC API KEY from https://www.anthropic.com/api

Copy over the `.env` example with 
```bash
cd ai_podcast_generator && cp .env.example .env
```
and paste over your API key. 

* Install the python requirements:
```bash
pip install -r requirements.txt
```

That's it!. This project is meant to be super minimal. 

## Set up your configs
* Open `configs.py`
* There will be the following:
```python
PODCAST_TOPICS = [
    "topic 1 ",
    "topic 2",
    "...."
]


EPISODE_DURATION_MINUTES = 15 # not precise
HOST_1_NAME = "Alice" # name of the first host, default female voice
HOST_2_NAME = "Bob" # name of the first host, default male voice
OPEN_AI_MODEL= "gpt-4o-mini" # your choice of the open_ai model
CLAUDE_MODEL = "claude-2.1" # your choice of the claude model 
MODEL = 1 # 0 is OpenAI and 1 is Claude
```
* OpenAI models can be found: https://platform.openai.com/docs/models
* Claude models can be found: https://docs.anthropic.com/en/docs/about-claude/models


## Run the program
`python3 main.py`
* This will create an mp3 file based on a random topic in your topic list. 

### Common errors:
There is a slight chance when you run the program you are greeted with:
```
Parsed lines: []

Error: No audio files were generated. Check the content and TTS process.
```
There are two things to try:
* Re-run the program
* Change your podcast topics, there might be one that is not working well