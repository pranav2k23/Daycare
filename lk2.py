import speech_recognition as sr
from pydub import AudioSegment

# Convert MP3 to WAV
audio = AudioSegment.from_mp3("aa.mp3")
audio.export("audio.wav", format="wav")

# Recognize speech
recognizer = sr.Recognizer()
with sr.AudioFile("audio.wav") as source:
    audio_data = recognizer.record(source)

# Convert to text
text = recognizer.recognize_google(audio_data)
print("Transcription:", text)
