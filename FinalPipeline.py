import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from divideAudio import split_audio
from multipleVideos import process_audio_chunks
from translateText import translate_text
from translateTextLLMs import translate_text_Gemini, translate_text_Llama3
from evaluateTranslations import  evaluate_translation_metrics

def extract_audio_from_video(video_file):
    """Extract audio from a video file and save it as a .wav file."""
    video = VideoFileClip(video_file)
    audio = video.audio
    audio_file = os.path.splitext(video_file)[0] + ".wav"
    audio.write_audiofile(audio_file)
    return audio_file

def ensure_wav_format(input_file):
    """Converts the input audio file to .wav format if it's not already."""
    if not input_file.endswith(".wav"):
        output_file = os.path.splitext(input_file)[0] + ".wav"
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format="wav")
        return output_file
    return input_file

def check_audio_length_and_process(audio_file):
    """Checks if the audio is longer than 15 seconds and processes it accordingly."""
    audio = AudioSegment.from_file(audio_file)
    if len(audio) > 15000:  # 15 seconds in milliseconds
        # Split audio into chunks
        out_dir = split_audio(audio_file)
        return out_dir
    else:
        print(f"Audio file '{audio_file}' is less than 15 seconds, skipping splitting.")
    

def run_pipeline(input_file):
    """Main pipeline function."""
    
    # Extract audio from video if input is a video file
    if input_file.endswith(('.mp4', '.mov', '.avi', '.mkv')):
        print(f"Extracting audio from video: {input_file}")
        audio_file = extract_audio_from_video(input_file)
    else:
        audio_file = input_file

    # Ensure the file is in .wav format
    wav_file = ensure_wav_format(audio_file)
    
    # Check if the audio is longer than 15 seconds and split if necessary
    # Directory where audio chunks are saved
    chunk_directory = check_audio_length_and_process(wav_file)
    
    # Process audio chunks
    full_transcription, all_segments = process_audio_chunks(chunk_directory)

    print("Original Text: ", full_transcription)
    
    # Translate the generated text
    target_language = 'french'  # Example target language (French)
    
    translated_text = translate_text(full_transcription,target_language)
    print('\n')

    translated_text_Gemini = translate_text_Gemini(full_transcription, target_language)
    print('\n')
    
    translated_text_llama3 = translate_text_Llama3(full_transcription, target_language)
    print('\n')

    # Print and save the translated text
    print("Translated Text with normal Translator:", translated_text)
    with open("translated_text.txt", "w") as f:
        f.write(translated_text)

    print("Translated Text with Gemini:", translated_text_Gemini)
    with open("translated_text_Gemini.txt", "w") as f:
        f.write(translated_text_Gemini)

    print("Translated Text with Llama3:", translated_text_llama3)
    with open("translated_text_Llama3.txt", "w") as f:
        f.write(translated_text_Gemini)

    print('\n')

    # Evaluate
    # 1. Gemini w.r.t Normal Google Translator
    print("Gemini vs Google Translator")
    Gemini_Norm_metric = evaluate_translation_metrics(translated_text_Gemini, translated_text)
    print(Gemini_Norm_metric)
    print('\n')

    # 2. Llama3 w.r.t Normal Google Translator
    print("Llama3 vs Google Translator")
    Llama3_Norm_metric=evaluate_translation_metrics(translated_text_llama3, translated_text)
    print(Llama3_Norm_metric)
    print('\n')

    # 1. Gemini w.r.t Llama3
    print("Gemini vs Llama3")
    Gemini_Llama_metric=evaluate_translation_metrics(translated_text_Gemini, translated_text_llama3)
    print(Gemini_Llama_metric)
    print('\n')

# Run the pipeline with the input file (either audio or video)
input_file = "RawVideos\EggRolls.mp4"  # Provide the path to your audio or video file
run_pipeline(input_file)
