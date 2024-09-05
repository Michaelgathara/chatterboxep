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

def parse_content(content, host1_name, host2_name):
    lines = content.split('\n')
    parsed_lines = []
    for line in lines:
        if line.startswith(f"{host1_name}:") or line.startswith(f"{host2_name}:"):
            speaker, text = line.split(':', 1)
            parsed_lines.append((speaker.strip(), text.strip()))
    return parsed_lines

def text_to_speech(text, output_file, voice):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    with open(output_file, 'wb') as f:
        for chunk in response.iter_bytes():
            f.write(chunk)

def analyze_audio(file_path):
    audio = AudioSegment.from_mp3(file_path)
    duration = len(audio)
    # Implement silence detection and trimming if needed
    return audio, duration

def add_pause(audio, pause_duration=500):  # 500ms pause
    return audio + AudioSegment.silent(duration=pause_duration)

def combine_audio_files(audio_segments):
    return sum(audio_segments, AudioSegment.empty())

def verify_voices(audio_files):
    host1_duration = sum(len(audio) for audio, host in audio_files if host == HOST_1_NAME)
    host2_duration = sum(len(audio) for audio, host in audio_files if host == HOST_2_NAME)
    total_duration = host1_duration + host2_duration
    host1_percentage = (host1_duration / total_duration) * 100
    host2_percentage = (host2_duration / total_duration) * 100
    print(f"{HOST_1_NAME} speaks for {host1_percentage:.2f}% of the time")
    print(f"{HOST_2_NAME} speaks for {host2_percentage:.2f}% of the time")
    return abs(host1_percentage - host2_percentage) < 20  # Allow 20% difference

def generate_episode():
    topic = random.choice(PODCAST_TOPICS)
    content = generate_podcast_content(topic, EPISODE_DURATION_MINUTES, HOST_1_NAME, HOST_2_NAME)
    parsed_lines = parse_content(content, HOST_1_NAME, HOST_2_NAME)

    audio_files = []
    for i, (speaker, text) in enumerate(parsed_lines):
        output_file = f"temp_audio_{i}.mp3"
        voice = "nova" if speaker == HOST_1_NAME else "echo"
        text_to_speech(text, output_file, voice)
        audio, duration = analyze_audio(output_file)
        audio_files.append((add_pause(audio), speaker))
        os.remove(output_file)

    if not verify_voices(audio_files):
        print("Voice distribution is uneven. Regenerating content...")
        return generate_episode()  # Recursively try again

    final_audio = combine_audio_files([audio for audio, _ in audio_files])
    
    if os.path.exists("intro.mp3") and os.path.exists("outro.mp3"):
        intro = AudioSegment.from_mp3("intro.mp3")
        outro = AudioSegment.from_mp3("outro.mp3")
        final_audio = intro + final_audio + outro

    output_filename = f"AI_Podcast_Episode_{topic.replace(' ', '_')}.mp3"
    final_audio.export(output_filename, format="mp3")
    print(f"Podcast episode generated and saved as {output_filename}")

if __name__ == "__main__":
    generate_episode()