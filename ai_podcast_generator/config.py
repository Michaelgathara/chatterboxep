import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_KEY = os.getenv('ANTHROPIC_KEY')

PODCAST_TOPICS = [
    "A debate on whether AI will be good for humanity or not"
]


EPISODE_DURATION_MINUTES = 15

HOST_1_NAME = "Alice"
HOST_1_VOICE = "nova"

HOST_2_NAME = "Bob"
HOST_2_VOICE = "echo"

USER_CHOICE_MODEL = 0 # 0 is OpenAI and 1 is Claude
OPEN_AI_MODEL= "gpt-5-nano"
CLAUDE_MODEL = "claude-3-5-sonnet-latest"