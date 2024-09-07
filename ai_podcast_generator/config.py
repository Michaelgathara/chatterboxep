import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_KEY = os.getenv('ANTHROPIC_KEY')

PODCAST_TOPICS = [
    "Artificial Intelligence",
    "Machine Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Robotics",
    "Podcasts made by AI's",
    "AI and Cybersecurity: Strengthening Defense Against Digital Threats",
    "The Role of AI in Personalized Education",
    "AI in Gaming: From NPCs to Procedural Generation",
    "Edge AI: Bringing Artificial Intelligence to the Device Level",
    "The Role of AI in Space Exploration: From Autonomous Rovers to Predictive Analysis"
]


EPISODE_DURATION_MINUTES = 15
HOST_1_NAME = "Alice"
HOST_2_NAME = "Bob"