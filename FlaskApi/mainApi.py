from flask import Flask, request, jsonify
import librosa
import speech_recognition as sr
import os

app = Flask(__name__)


@app.route('/AudioToText', methods=['POST'])
def audio_to_text():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Load audio with librosa
        audio_data, sr_rate = librosa.load(file_path, sr=None)

        # Convert audio to text using SpeechRecognition
        recognizer = sr.Recognizer()
        audio = sr.AudioFile(file_path)

        with audio as source:
            audio_content = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_content)
        except sr.UnknownValueError:
            text = "Could not understand audio"
        except sr.RequestError as e:
            text = f"Could not request results; {e}"

        # Clean up the uploaded file
        os.remove(file_path)

        return jsonify({"text": text})


if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(host='0.0.0.0', port=8080)
