# chatterboxep

Generate two‑host AI podcast episodes and export them as MP3.

## Pre‑reqs
- OpenAI API key (for script + TTS). Get one from [OpenAI](https://platform.openai.com/).
- Optional: Anthropic API key (for script via Claude). Get one from [Anthropic](https://www.anthropic.com/api).
- ffmpeg installed and on your PATH (required by `pydub` for MP3 I/O).

## Setup
```bash
# from project root
pip install -r requirements.txt
```

Create an `.env` file inside `ai_podcast_generator/`:
```bash
# ai_podcast_generator/.env
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_KEY=your_anthropic_api_key   # optional if using Claude
```

## Configure
Edit `ai_podcast_generator/config.py`:
```python
PODCAST_TOPICS = [
    "Your topic 1",
    "Your topic 2",
]

EPISODE_DURATION_MINUTES = 15
HOST_1_NAME = "Alice"
HOST_2_NAME = "Bob"
OPEN_AI_MODEL = "gpt-4o-mini"
CLAUDE_MODEL = "claude-2.1"
USER_CHOICE_MODEL = 0  # 0 = OpenAI, 1 = Claude
```
- OpenAI model list: [OpenAI models](https://platform.openai.com/docs/models)
- Claude model list: [Claude models](https://docs.anthropic.com/en/docs/about-claude/models)

Notes:
- Host 1 uses OpenAI TTS voice `nova`; Host 2 uses `echo` (see `config.py` if you want to change).
- `EPISODE_DURATION_MINUTES` scales token limits; final audio length is approximate.

## Run
```bash
cd ai_podcast_generator
python main.py   # on Windows: python main.py or py -3 main.py
```
This creates an MP3 named like `AI_Podcast_Episode_<Topic_With_Underscores>.mp3` in the current directory.

If `intro.mp3` and/or `outro.mp3` are present in the same directory, they will be prepended/appended to the episode automatically. These can be used for intro/outro music/introductions

## Troubleshooting
- Parsed lines are empty or no audio generated:
  - Rerun the program.
  - Try a different topic; the parser expects lines like `Alice: ...` / `Bob: ...`.
- `pydub`/ffmpeg errors: ensure ffmpeg is installed and accessible on your PATH.

## Why two providers?
- OpenAI: used for both script (Chat Completions) and text‑to‑speech (TTS `tts-1-hd`).
- Anthropic (optional): can generate the script instead of OpenAI if `USER_CHOICE_MODEL = 1`.