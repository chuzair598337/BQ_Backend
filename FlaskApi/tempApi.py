
from flask import Flask, request, jsonify
import os
from pydub import AudioSegment
from flask import jsonify

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



    #result = processVoiceCommand(wav_file_path)

    result = [
        {"key1": "Play"},  # 0
        {"key1": "Pause"},  # 1
        {"key1": "Repeat"},  # 2
        {"key1": "Next"},  # 3
        {"key1": "Previous"},  # 4
        {"key1": "Play", "key2": "Al-Fatiha"},  # 5 (Surah 1)
        {"key1": "Play", "key2": "Al-Baqarah"},  # 6 (Surah 2)
        {"key1": "Play", "key2": "Aal-E-Imran"},  # 7 (Surah 3)
        {"key1": "Play", "key2": "An-Nisa"},  # 8 (Surah 4)
        {"key1": "Play", "key2": "Al-Maidah"}  # 9 (Surah 5)
    ]

    # return jsonify({"text": result})
    return jsonify(result[5])


def save_audio(file):
    file_path = os.path.join("uploads", file.filename)
    try:
        file.save(file_path)
        return file_path, True
    except Exception as e:
        print(f"Failed to save file: {e}")
        return None, False

def convert_audio_to_wav(file_path):
    # Extract file extension (e.g., "m4a", "ogg", "aac")
    file_extension = file_path.split('.')[-1]

    if os.path.exists(file_path):
        # Define the new file path with a ".wav" extension
        wav_file_path = file_path.replace(f".{file_extension}", ".wav")

        try:
            # Load the audio file in its original format
            audio = AudioSegment.from_file(file_path, format=file_extension)

            # Export the audio to WAV format
            audio.export(wav_file_path, format="wav")

            # Optionally, remove the original file
            os.remove(file_path)

            return wav_file_path
        except Exception as e:
            print(f"Failed to convert {file_extension} file: {e}")
            return None
    else:
        print(f"File not found at {file_path}")
        return None

if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(host='0.0.0.0', port=8080)
