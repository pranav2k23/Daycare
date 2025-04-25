def veidosumma(mp4path):
    from datetime import datetime
    fame = datetime.now().strftime("%Y%m%d%H%M%S")

    from audio_extract import extract_audio
    # import whisper
    extract_audio(input_path=mp4path,
                  output_path=fame + ".mp3")

    import speech_recognition as sr
    from pydub import AudioSegment

    mp3_file = fame + ".mp3"  # Change this to your file path
    wav_file = fame + ".wav"
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")

    # Initialize recognizer
    recognizer = sr.Recognizer()

    text = ""
    # Load the WAV file
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file
    # Convert audio to text using Google's Speech Recognition
    try:
        text = recognizer.recognize_google(audio_data)
        print("Transcription:", text)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError:
        print("Could not request results, check internet connection")


    from transformers import pipeline

    # Load the summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Generate summary
    summary = summarizer(text, max_length=50, min_length=20, do_sample=False)

    # Output the summary
    print(summary[0]['summary_text'])


veidosumma(r"C:\Users\prana\Downloads\Preschool\Preschool\media\videos\a.mp4")