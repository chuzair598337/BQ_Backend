from flask import Flask, request, jsonify
import librosa
import speech_recognition as sr
import os
from AudioHandler import *

app = Flask(__name__)


@app.route('/AudioToText', methods=['POST'])
def audio_to_text():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save the audio file
    m4a_file_path, success = save_audio(file)
    if not success:
        return "Failed to save file", 500

    # Convert audio to wav if necessary
    if file.mimetype == "audio/m4a":
        wav_file_path = convert_m4a_to_wav(m4a_file_path)
        if not wav_file_path:
            return "Failed to convert m4a to wav", 500
    # add other formats here



    result = processVoiceCommand(wav_file_path)

    return jsonify({"text": result})


if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(host='0.0.0.0', port=8080)
