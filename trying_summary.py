import moviepy.editor as mp
import speech_recognition as sr
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer

def extract_audio_from_video(video_path, audio_path="audio.wav"):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    print(f"Audio extracted to {audio_path}")

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        print(f"Transcription: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError:
        print("Speech recognition request failed.")
        return ""

def summarize_text(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, PlaintextParser.from_string(text))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    summarized_text = ' '.join([str(sentence) for sentence in summary])
    return summarized_text

def video_text_summary(video_path):
    audio_path = "audio.wav"
    extract_audio_from_video(video_path, audio_path)
    transcribed_text = transcribe_audio(audio_path)
    
    if transcribed_text:
        summary = summarize_text(transcribed_text)
        print("Summary:")
        print(summary)
    else:
        print("No transcription available.")

# Example usage:
# video_path = r"C:\Users\prana\Downloads\Preschool\Preschool\media\videos\20250328-180901.mp4"
video_path = r"C:\Users\prana\Downloads\Preschool\Preschool\media\videos\20250328-175607.mp4"
video_text_summary(video_path)
