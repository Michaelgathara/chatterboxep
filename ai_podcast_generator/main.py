import random, os, shutil
from pydub import AudioSegment
from openai import OpenAI
from config import OPENAI_API_KEY, PODCAST_TOPICS, EPISODE_DURATION_MINUTES, HOST_1_NAME, HOST_2_NAME

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_podcast_content(topic, duration_minutes, host1_name, host2_name):
    prompt = f"""Create a {duration_minutes}-minute podcast script about {topic}. 
    The podcast should be a conversation between two hosts: {host1_name} (female) and {host2_name} (male).
    Include an introduction, main content, and conclusion. Format the script as follows:

    {host1_name}: [Host 1's dialogue]
    {host2_name}: [Host 2's dialogue]
    
    Repeat this pattern for the entire conversation."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates realistic sounding podcast scripts."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=duration_minutes * 150,
        n=1,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def text_to_speech(text, output_file, voice):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    response.stream_to_file(output_file)

def combine_audio_files(file_list, output_file):
    combined = AudioSegment.empty()
    for file in file_list:
        audio = AudioSegment.from_mp3(file)
        combined += audio
    combined.export(output_file, format="mp3")

def add_intro_outro(audio_file, intro_file, outro_file):
    podcast = AudioSegment.from_mp3(audio_file)
    intro = AudioSegment.from_mp3(intro_file)
    outro = AudioSegment.from_mp3(outro_file)
    
    final_podcast = intro + podcast + outro
    return final_podcast

def generate_episode():
    topic = random.choice(PODCAST_TOPICS)
    content = generate_podcast_content(topic, EPISODE_DURATION_MINUTES, HOST_1_NAME, HOST_2_NAME)

    print(f"Generated content for topic: {topic}")
    print(content)

    
    temp_folder = "temp_audio"
    os.makedirs(temp_folder, exist_ok=True)

    try:
        
        lines = content.split('\n')
        audio_files = []

        for i, line in enumerate(lines):
            if ':' in line:
                host, text = line.split(':', 1)
                host = host.strip()
                text = text.strip()

                if text:  
                    output_file = os.path.join(temp_folder, f"audio_{i}.mp3")
                    voice = "nova" if host == HOST_1_NAME else "echo"
                    text_to_speech(text, output_file, voice)
                    audio_files.append(output_file)

        
        combined_file = os.path.join(temp_folder, "combined_audio.mp3")
        combine_audio_files(audio_files, combined_file)

        
        if os.path.exists("intro.mp3") and os.path.exists("outro.mp3"):
            final_podcast = add_intro_outro(combined_file, "intro.mp3", "outro.mp3")
        else:
            print("Warning: intro.mp3 or outro.mp3 not found. Skipping intro/outro addition.")
            final_podcast = AudioSegment.from_mp3(combined_file)

        
        output_filename = f"AI_Podcast_Episode_{topic.replace(' ', '_')}.mp3"
        final_podcast.export(output_filename, format="mp3")

        print(f"Podcast episode generated and saved as {output_filename}")

    except Exception as e:
        print(f"An error occurred while generating the podcast: {str(e)}")
        # Optionally, save the generated text content in case of audio generation failure
        with open(f"AI_Podcast_Episode_{topic.replace(' ', '_')}.txt", "w") as f:
            f.write(content)
        print(f"Podcast content saved as text in AI_Podcast_Episode_{topic.replace(' ', '_')}.txt")

    finally:
        # Clean up: remove the temporary folder and its contents
        shutil.rmtree(temp_folder, ignore_errors=True)

if __name__ == "__main__":
    generate_episode()