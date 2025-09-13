class Prompts:
    def __init__(self, topic, duration, host1_name, host2_name):
        self.topic = topic
        self.duration = duration
        self.host1_name = host1_name
        self.host2_name = host2_name
        
    def get_podcast_prompt(self):
        return\
            f"""Create a {self.duration}-minute podcast script about {self.topic}. 
                The podcast should be a conversation between two hosts: {self.host1_name} (female) and {self.host2_name} (male).
                Include an introduction, main content, and conclusion. Format the script as follows:

                {self.host1_name}: [Host 1's dialogue]
                {self.host2_name}: [Host 2's dialogue]
    
                Repeat this pattern for the entire conversation."""
    
    def get_system_role(self):
        return f""""You write realistic, broadcast-quality podcast dialogue between two hosts. Output must be ONLY a sequence of dialogue lines, each starting with the speaker name followed by a colon and a space, e.g.:
            Alice: ...
            Bob: ...
            No headings, stage directions, lists, scene breaks, or narrator lines. No text before the first line or after the last line.

            Style:
            - Natural spoken language, concise sentences, strong punctuation.
            - Occasional light humor and warmth; avoid slapstick.
            - Use interjections or onomatopoeia (e.g., “ha!”, “hehe”) for laughter; do NOT use bracketed tags like [laugh].
            - Avoid emojis and unusual symbols. No excessive capitalization.

            Structure and pacing:
            - Alternate turns strictly. Keep speaking time roughly balanced.
            - Use a clear arc: brief hook, exploration, concrete examples, occasional clarifications, and a short wrap-up.
            - Prefer 20-35 words per turn. Avoid very long monologues.

            Safety and tone:
            - Be factual where possible, avoid misinformation, and flag uncertainty briefly.
            - Keep content broadly suitable for a general audience."""