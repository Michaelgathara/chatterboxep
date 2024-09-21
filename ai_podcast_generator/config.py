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
HOST_2_NAME = "Bob"
OPEN_AI_MODEL= "gpt-4o-mini"
CLAUDE_MODEL = "claude-2.1"
USER_CHOICE_MODEL = 0 # 0 is OpenAI and 1 is Claude