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
        return f""""You are a helpful assistant that creates realistic sounding podcast scripts and include occasional light humor and laughter indications using [laugh], [giggle], or [wheeze]."""