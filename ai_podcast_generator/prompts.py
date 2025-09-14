class Prompts:
    def __init__(self, topic, duration, host1_name, host2_name):
        self.topic = topic
        self.duration = duration
        self.host1_name = host1_name
        self.host2_name = host2_name
        
    def get_podcast_prompt(self):
        return\
            f"""Create a {self.duration}-minute podcast conversation about: {self.topic}

            Hosts:
            - {self.host1_name} (female)
            - {self.host2_name} (male)

            Constraints:
            - Output ONLY dialogue lines in this exact format:
            {self.host1_name}: ...
            {self.host2_name}: ...
            - Alternate speakers every line; no other speakers.
            - No headings, narrator lines, stage directions, or meta text.
            - Do NOT use bracketed tags like [laugh]; use natural interjections (e.g., ha!, hehe) if needed.
            - Do NOT include colons in the dialogue content (only after the speaker name).
            - Keep sentences short and conversational. Prefer 20-35 words per line.
            - Begin immediately with the first line by {self.host1_name}.

            Pacing targets (approximate):
            - Total words: ~{int(self.duration * 160)}
            - Total lines: ~{int(self.duration * 160 / 30)}
            - Keep speaking time roughly balanced between hosts.
            """
    
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