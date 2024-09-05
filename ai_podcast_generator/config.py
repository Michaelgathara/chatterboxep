import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PODCAST_TOPICS = [
    "Podcasts made by AI's"
]
# PODCAST_TOPICS = [
#     "Artificial Intelligence",
#     "Machine Learning",
#     "Natural Language Processing",
#     "Computer Vision",
#     "Robotics"
# ]
EPISODE_DURATION_MINUTES = 5
HOST_1_NAME = "Alice"
HOST_2_NAME = "Bob"