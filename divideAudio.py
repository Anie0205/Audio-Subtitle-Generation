import os
from pydub import AudioSegment

def split_audio(audio_file):
    """Splits the audio into 10-second chunks and saves them in a directory named after the video file."""
    
    # Load the audio file
    audio = AudioSegment.from_file(audio_file)
    
    # Get the base name (file name without extension)
    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    
    # Define the output directory (name it after the video file)
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), base_name)
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Split the audio into 10-second chunks (10,000 ms per chunk)
    chunk_length_ms = 10000  # 10 seconds in milliseconds
    num_chunks = len(audio) // chunk_length_ms + (1 if len(audio) % chunk_length_ms != 0 else 0)
    
    for i in range(num_chunks):
        start_ms = i * chunk_length_ms
        end_ms = min((i + 1) * chunk_length_ms, len(audio))
        chunk = audio[start_ms:end_ms]
        
        # Save chunk as a .wav file in the output directory
        chunk.export(os.path.join(output_dir, f"{base_name}_chunk{i + 1}.wav"), format="wav")
    
    print(f"Audio successfully split into {num_chunks} chunks and saved in '{output_dir}'.")
    return output_dir

