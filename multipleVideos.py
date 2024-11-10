import os
import requests
import json
from pydub import AudioSegment

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
headers = {"Authorization": "Bearer API KEY"}

def get_audio_chunks(directory):
    # List all .wav files in the specified directory
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.wav')]

def query_chunk(chunk):
    with open(chunk, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)

    print("Response status code:", response.status_code)

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("text", ""), response_data.get("segments", [])
    else:
        print("Error:", response.text)
        return None, []

def process_audio_chunks(chunk_directory):
    chunks = get_audio_chunks(chunk_directory)
    full_transcription = ""
    all_segments = []

    for i, chunk in enumerate(chunks):
        text, segments = query_chunk(chunk)
        full_transcription += text + " "  # Combine transcriptions
        
        # Append segments with adjusted timestamps
        for segment in segments:
            adjusted_start = segment['start'] + (i * 30)  # Assuming each chunk is approximately 30 seconds
            adjusted_end = segment['end'] + (i * 30)
            segment['start'] = adjusted_start
            segment['end'] = adjusted_end
            all_segments.append(segment)

    return full_transcription.strip(), all_segments

# Example usage
#chunk_directory = "ExtractedAudio/short2"  # Adjust path as needed
#full_transcription, all_segments = process_audio_chunks(chunk_directory)

# Print full transcription
#print("Full Transcription:", full_transcription)

# Print segments with timestamps
#for segment in all_segments:
#    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s]: {segment['text']}")
