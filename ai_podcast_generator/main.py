import random, os, shutil
from pydub import AudioSegment
from openai import OpenAI
from config import (
    OPENAI_API_KEY,
    ANTHROPIC_KEY,
    PODCAST_TOPICS,
    EPISODE_DURATION_MINUTES,
    HOST_1_NAME,
    HOST_2_NAME,
    MODEL,
)
from anthropic import Anthropic

open_ai_client = OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = Anthropic(api_key=ANTHROPIC_KEY)


def generate_podcast_content_open_ai(topic, duration_minutes, host1_name, host2_name):
    prompt = f"""Create a {duration_minutes}-minute podcast script about {topic}. 
    The podcast should be a conversation between two hosts: {host1_name} (female) and {host2_name} (male).
    Include an introduction, main content, and conclusion. Format the script as follows:

    {host1_name}: [Host 1's dialogue]
    {host2_name}: [Host 2's dialogue]
    
    Repeat this pattern for the entire conversation."""

    response = open_ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that creates realistic sounding podcast scripts and include occasional light humor and laughter indications using [laugh], [giggle], or [wheeze].",
            },
            # https://github.com/YuanGongND/whisper-at/issues/7
            {"role": "user", "content": prompt},
        ],
        max_tokens = duration_minutes * 150,
        n = 1,
        temperature = 0.7,
    )
    return response.choices[0].message.content.strip()


def generate_podcast_content_claude(topic, duration_minutes, host1_name, host2_name):
    prompt = f"""Create a {duration_minutes}-minute podcast script about {topic}. 
    The podcast should be a conversation between two hosts: {host1_name} (female) and {host2_name} (male).
    Include an introduction, main content, and conclusion. Format the script as follows:

    {host1_name}: [Host 1's dialogue]
    {host2_name}: [Host 2's dialogue]
    
    Repeat this pattern for the entire conversation. Include occasional light humor and laughter indications using [laugh], [giggle], or [wheeze]."""

    response = anthropic_client.completions.create(
        model = "claude-2.1",
        max_tokens_to_sample = duration_minutes * 150,
        temperature = 0.7,
        prompt = f"{prompt}\n\nHuman: Please generate the podcast script as described above.\n\nAssistant:",
    )
    return response.completion.strip()


def parse_content(content, host1_name, host2_name):
    lines = content.split("\n")
    parsed_lines = []
    current_speaker = None
    current_text = []

    for line in lines:
        # print(f"Host 1: {host1_name}")
        # print(f"Host 2: {host2_name}")
        if line.startswith(f"{host1_name}:") or line.startswith(f"{host2_name}:"):
            print(f"Line: {line}")
            if current_speaker and current_text:
                parsed_lines.append((current_speaker, " ".join(current_text).strip()))
                current_text = []
            current_speaker = line.split(":", 1)[0].strip()
            current_text.append(line.split(":", 1)[1].strip())
        elif current_speaker:
            current_text.append(line.strip())

    if current_speaker and current_text:
        parsed_lines.append((current_speaker, " ".join(current_text).strip()))

    return parsed_lines


def text_to_speech(text, output_file, voice):
    response = open_ai_client.audio.speech.create(
        model = "tts-1", voice=voice, input=text
    )
    with open(output_file, "wb") as f:
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
    if not audio_files:
        print("Error: No audio files were generated.")
        return False

    host1_duration = sum(
        len(audio) for audio, host in audio_files if host == HOST_1_NAME
    )
    host2_duration = sum(
        len(audio) for audio, host in audio_files if host == HOST_2_NAME
    )
    total_duration = host1_duration + host2_duration

    if total_duration == 0:
        print("Error: Total audio duration is zero.")
        return False

    host1_percentage = (host1_duration / total_duration) * 100
    host2_percentage = (host2_duration / total_duration) * 100
    print(f"{HOST_1_NAME} speaks for {host1_percentage:.2f}% of the time")
    print(f"{HOST_2_NAME} speaks for {host2_percentage:.2f}% of the time")
    return abs(host1_percentage - host2_percentage) < 20  # Allow 20% difference


def generate_episode(model: int):
    topic = random.choice(PODCAST_TOPICS)
    if model == 0:
        content = generate_podcast_content_open_ai(
            topic, EPISODE_DURATION_MINUTES, HOST_1_NAME, HOST_2_NAME
        )
    if model == 1:
        content = generate_podcast_content_claude(
            topic, EPISODE_DURATION_MINUTES, HOST_1_NAME, HOST_2_NAME
        )
    parsed_lines = parse_content(content, HOST_1_NAME, HOST_2_NAME)

    # print(f"Generated content:\n{content}\n")
    print(f"Parsed lines: {parsed_lines}\n")

    audio_files = []
    for i, (speaker, text) in enumerate(parsed_lines):
        if not text.strip():
            print(f"Warning: Empty text for speaker {speaker} at line {i+1}")
            continue

        output_file = f"temp_audio_{i}.mp3"
        voice = "nova" if speaker == HOST_1_NAME else "echo"
        try:
            text_to_speech(text, output_file, voice)
            audio, duration = analyze_audio(output_file)
            audio_files.append((add_pause(audio), speaker))
            print(f"Generated audio for {speaker}: duration {duration}ms")
        except Exception as e:
            print(f"Error generating audio for line {i+1}: {e}")
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

    if not audio_files:
        print(
            "Error: No audio files were generated. Check the content and TTS process."
        )
        return

    if not verify_voices(audio_files):
        print(
            "Voice distribution is uneven or no audio generated. Regenerating content..."
        )
        return generate_episode(model = MODEL)

    final_audio = combine_audio_files([audio for audio, _ in audio_files])

    if os.path.exists("intro.mp3") and os.path.exists("outro.mp3"):
        intro = AudioSegment.from_mp3("intro.mp3")
        outro = AudioSegment.from_mp3("outro.mp3")
        final_audio = intro + final_audio + outro

    output_filename = f"AI_Podcast_Episode_{topic.replace(' ', '_')}.mp3"
    final_audio.export(output_filename, format="mp3")
    print(f"Podcast episode generated and saved as {output_filename}")


if __name__ == "__main__":
    generate_episode(model = MODEL)
