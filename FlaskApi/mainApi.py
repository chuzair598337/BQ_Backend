from flask import Flask, request, jsonify
import librosa
# import speech_recognition as sr
import os
from AudioHandler import *
from globalVariables import *


app = Flask(__name__)


@app.route('/Audio_Prediction', methods=['POST'])
def audio_Prediction():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save the audio file
    file_path, success = save_audio(file)
    if not success:
        return "Failed to save file", 500

    # Check content type and convert if necessary
    allowed_wav_formats = ['audio/vnd.wave', 'audio/wav', 'audio/wave', 'audio/x-wav']

    if file.content_type not in allowed_wav_formats:
        wav_file_path = convert_audio_to_wav(file_path)
        if not wav_file_path:
            return "Failed to convert your file format to wav", 500
    else:
        wav_file_path = file_path

    print(wav_file_path)

    result = processVoiceCommand(wav_file_path)

    return jsonify({"result":result})

if __name__ == '__main__':
    if not os.path.exists(ApiUpload):
        os.makedirs(ApiUpload)
    app.run(host='0.0.0.0', port=8080)
