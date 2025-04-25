# def veidosumma(mp4path):
#     from datetime import datetime
#     fame = datetime.now().strftime("%Y%m%d%H%M%S")
#
#     from audio_extract import extract_audio
#     # import whisper
#     extract_audio(input_path=mp4path,
#                   output_path=fame + ".mp3")
#
#     import speech_recognition as sr
#     from pydub import AudioSegment
#
#     mp3_file = fame + ".mp3"  # Change this to your file path
#     wav_file = fame + ".wav"
#     audio = AudioSegment.from_mp3(mp3_file)
#     audio.export(wav_file, format="wav")
#
#     # Initialize recognizer
#     recognizer = sr.Recognizer()
#
#     text = ""
#     # Load the WAV file
#     with sr.AudioFile(wav_file) as source:
#         audio_data = recognizer.record(source)  # Read the entire audio file
#     # Convert audio to text using Google's Speech Recognition
#     try:
#         text = recognizer.recognize_google(audio_data)
#         print("Transcription:", text)
#     except sr.UnknownValueError:
#         print("Could not understand the audio")
#     except sr.RequestError:
#         print("Could not request results, check internet connection")
#
#
#     from transformers import pipeline
#
#     # Load the summarization pipeline
#     summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#
#     # Generate summary
#     summary = summarizer(text, max_length=50, min_length=20, do_sample=False)
#
#     # Output the summary
#     return summary[0]['summary_text']
#
#
# # veidosumma(r"C:\Users\prana\Downloads\Preschool\Preschool\media\videos\a.mp4")
#
#
#
#
#
#
#
#




def veidosumma(mp4path):
    import os
    from datetime import datetime
    from audio_extract import extract_audio
    from pydub import AudioSegment
    import speech_recognition as sr
    from transformers import pipeline
    import math

    # Generate unique file name
    fame = datetime.now().strftime("%Y%m%d%H%M%S")

    # Step 1: Extract audio from mp4
    extract_audio(input_path=mp4path, output_path=fame + ".mp3")

    # Step 2: Convert MP3 to WAV
    mp3_file = fame + ".mp3"
    wav_file = fame + ".wav"
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")

    # Step 3: Transcribe long audio by splitting it into chunks
    def transcribe_large_audio(wav_file):
        recognizer = sr.Recognizer()
        audio = AudioSegment.from_wav(wav_file)

        chunk_length_ms = 60 * 1000  # 1 minute
        chunks = math.ceil(len(audio) / chunk_length_ms)

        full_text = ""

        for i in range(chunks):
            start = i * chunk_length_ms
            end = min((i + 1) * chunk_length_ms, len(audio))
            chunk = audio[start:end]
            temp_chunk_file = f"temp_chunk_{i}.wav"
            chunk.export(temp_chunk_file, format="wav")

            with sr.AudioFile(temp_chunk_file) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data)
                    full_text += " " + text
                except sr.UnknownValueError:
                    print(f"Chunk {i} could not be understood")
                except sr.RequestError as e:
                    print(f"Request error on chunk {i}: {e}")

            os.remove(temp_chunk_file)  # Cleanup temporary file

        return full_text.strip()

    text = transcribe_large_audio(wav_file)
    if not text:
        return "Could not transcribe any audio."

    print("Full Transcription:", text)

    # Step 4: Summarize long text
    def summarize_long_text(text, chunk_size=1000):
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        summary = ""
        for chunk in chunks:
            sm = summarizer(chunk, max_length=50, min_length=20, do_sample=False)
            summary += sm[0]['summary_text'] + " "
        return summary.strip()

    summary = summarize_long_text(text)

    # Optional cleanup
    os.remove(mp3_file)
    os.remove(wav_file)

    return summary

# Example usage:
# summary_result = veidosumma(r"C:\Path\To\Your\Video.mp4")
# print("SUMMARY:\n", summary_result)
