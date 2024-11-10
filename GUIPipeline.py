import sqlite3
import os
import tkinter as tk
from tkinter import filedialog, Text, messagebox
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from divideAudio import split_audio
from multipleVideos import process_audio_chunks
from translateText import translate_text
from translateTextLLMs import translate_text_Gemini, translate_text_Llama3
from evaluateTranslations import evaluate_translation_metrics

# Database setup
def init_db():
    conn = sqlite3.connect("translations.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS translations (
                        id INTEGER PRIMARY KEY,
                        video_name TEXT,
                        transcript_file TEXT,
                        translated_text_google TEXT,
                        translated_text_gemini TEXT,
                        translated_text_llama3 TEXT)''')
    conn.commit()
    conn.close()

def save_to_db(video_name, transcript, google_translation, gemini_translation, llama3_translation):
    conn = sqlite3.connect("translations.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO translations (video_name, transcript_file, translated_text_google, 
                      translated_text_gemini, translated_text_llama3) VALUES (?, ?, ?, ?, ?)''', 
                   (video_name, transcript, google_translation, gemini_translation, llama3_translation))
    conn.commit()
    conn.close()

def extract_audio_from_video(video_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio_file = os.path.splitext(video_file)[0] + ".wav"
    audio.write_audiofile(audio_file)
    return audio_file

def ensure_wav_format(input_file):
    if not input_file.endswith(".wav"):
        output_file = os.path.splitext(input_file)[0] + ".wav"
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format="wav")
        return output_file
    return input_file

def check_audio_length_and_process(audio_file):
    audio = AudioSegment.from_file(audio_file)
    if len(audio) > 15000:
        out_dir = split_audio(audio_file)
        return out_dir
    else:
        messagebox.showinfo("Info", f"Audio file '{audio_file}' is less than 15 seconds, skipping splitting.")
        return None

def run_pipeline(input_file, target_language, output_text):
    if input_file.endswith(('.mp4', '.mov', '.avi', '.mkv')):
        audio_file = extract_audio_from_video(input_file)
    else:
        audio_file = input_file

    wav_file = ensure_wav_format(audio_file)
    chunk_directory = check_audio_length_and_process(wav_file)
    if not chunk_directory:
        return

    full_transcription, all_segments = process_audio_chunks(chunk_directory)
    output_text.insert(tk.END, f"Original Text: {full_transcription}\n\n")
    
    translated_text = translate_text(full_transcription, target_language)
    translated_text_Gemini = translate_text_Gemini(full_transcription, target_language)
    translated_text_llama3 = translate_text_Llama3(full_transcription, target_language)

    output_text.insert(tk.END, f"Translated Text with Google Translator: {translated_text}\n")
    output_text.insert(tk.END, f"Translated Text with Gemini: {translated_text_Gemini}\n")
    output_text.insert(tk.END, f"Translated Text with Llama3: {translated_text_llama3}\n\n")

    # Save to database
    video_name = os.path.basename(input_file)
    save_to_db(video_name, full_transcription, translated_text, translated_text_Gemini, translated_text_llama3)

    output_text.insert(tk.END, "Data saved to database.\n")

def select_file(file_entry):
    file_path = filedialog.askopenfilename(filetypes=[("Video/Audio Files", "*.mp4 *.mov *.avi *.mkv *.wav")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def main():
    # Initialize the database
    init_db()
    
    root = tk.Tk()
    root.title("Audio-Video Translation Pipeline")

    tk.Label(root, text="Select Video/Audio File").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    file_entry = tk.Entry(root, width=40)
    file_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_file(file_entry)).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(root, text="Target Language").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    target_language_entry = tk.Entry(root, width=15)
    target_language_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    target_language_entry.insert(0, "french")  # Default language

    output_text = Text(root, wrap="word", width=80, height=20)
    output_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    tk.Button(root, text="Start Process", command=lambda: run_pipeline(file_entry.get(), target_language_entry.get(), output_text)).grid(row=2, column=1, padx=10, pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
