# api/transcribe.py
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
import os
import uuid

# Set FFmpeg and FFprobe paths explicitly
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

def convert_mp3_to_wav(mp3_file_path):
    sound = AudioSegment.from_mp3(mp3_file_path)
    wav_file_path = mp3_file_path.replace(".mp3", f"_{uuid.uuid4().hex}.wav")
    sound.export(wav_file_path, format="wav")
    return wav_file_path

def convert_webm_to_wav(webm_file_path):
    print(f"Converting WebM to WAV: {webm_file_path}")
    sound = AudioSegment.from_file(webm_file_path, format="webm")
    wav_file_path = webm_file_path.replace(".webm", ".wav")
    sound.export(wav_file_path, format="wav")
    print(f"Converted WAV Path: {wav_file_path}")
    return wav_file_path

def transcribe_audio(file):
    recognizer = sr.Recognizer()
    
    # Save uploaded file temporarily
    temp_webm_path = f"temp_audio_{uuid.uuid4().hex}.webm"
    with open(temp_webm_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)
    
    print(f"Temp WebM Path: {temp_webm_path}")
    print(f"Does file exist? {os.path.exists(temp_webm_path)}")

    # Convert WebM to WAV
    wav_path = convert_webm_to_wav(temp_webm_path)

    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Transcribed Text: {text}")
        except sr.UnknownValueError:
            text = "Could not understand audio"
            print("Speech Recognition Error: Could not understand audio")
        except sr.RequestError:
            text = "Speech recognition service unavailable"
            print("Speech Recognition Error: Service unavailable")

    # Clean up
    os.remove(temp_webm_path)
    os.remove(wav_path)

    return text
