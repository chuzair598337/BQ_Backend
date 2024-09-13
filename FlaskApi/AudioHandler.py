import os
from pydub import AudioSegment
from flask import jsonify
import librosa
import speech_recognition as sr
import shutil
from pydub.silence import split_on_silence, detect_leading_silence
import tensorflow as tf
import numpy as np

from globalVariables import *

model_path = os.path.join(data_Folder,ModelName)

# def extract_features(file_name):
#     # Load the audio file using librosa
#     y, sr = librosa.load(file_name, sr=None)
#
#     # Extract features (e.g., MFCCs, Chroma, Mel spectrogram, etc.)
#     # We'll extract 40 MFCCs (Mel-frequency cepstral coefficients)
#     mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
#
#     # Flatten the MFCCs to create a single feature vector
#     mfccs_scaled = np.mean(mfccs.T, axis=0)
#
#     # Ensure we have 1408 features by resizing or padding
#     feature_vector = np.resize(mfccs_scaled, (1408,))
#
#     return feature_vector

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)

    # Extract features (e.g., MFCCs, Chroma, Mel spectrogram, etc.)
    # We'll extract 40 MFCCs (Mel-frequency cepstral coefficients)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)

    # Flatten the MFCCs to create a single feature vector
    mfccs_scaled = np.mean(mfccs.T, axis=0)

    # Ensure we have 1408 features by resizing or padding
    feature_vector = np.resize(mfccs_scaled, (1408,))

    return feature_vector

def cleanAudioFromStartandEnd(audio_segment, silence_thresh=-50.0, chunk_size=10):
    """
    Removes silence from the beginning and end of the audio_segment.

    audio_segment - the AudioSegment to process
    silence_thresh - the upper bound for how quiet is silent in dBFS
    chunk_size - chunk size for iterating over the segment in ms
    """
    # Detect leading silence
    start_trim = detect_leading_silence(audio_segment, silence_thresh, chunk_size)

    # Reverse the audio and detect leading silence again to find the end trim
    reversed_audio = audio_segment.reverse()
    end_trim = detect_leading_silence(reversed_audio, silence_thresh, chunk_size)

    # Calculate the duration to keep (without silence)
    duration = len(audio_segment) - start_trim - end_trim

    # Get the trimmed audio segment
    trimmed_audio = audio_segment[start_trim:start_trim + duration]

    # Save the trimmed audio segment to a file
    trimmed_audio.export("trimmedFile.wav", format="wav")

    # Print duration in milliseconds
    duration_ms = len(trimmed_audio)
    print(f"Duration of the trimmed audio: {duration_ms} ms")

    # Return the trimmed audio segment
    return trimmed_audio


def loadAudio(audio_path):
    try:
        # Load the audio file
        audio = AudioSegment.from_wav(audio_path)
        return audio
    except FileNotFoundError:
        print(f"Error: The file {audio_path} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred while loading the audio file: {e}")
        return []


def split_audio_on_silence(audio, min_silence_len=500, silence_thresh=-40, output_dir="output"):
    # Split audio where the silence is longer than min_silence_len and silence is quieter than silence_thresh
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        shutil.rmtree(output_dir)  # Remove the directory and all its contents
        os.makedirs(output_dir)

    word_files = []

    # Export each chunk as a separate file, overwriting existing files if present
    for i, chunk in enumerate(chunks):
        word_file_name = f"command_{i + 1}.wav"
        output_path = os.path.join(output_dir, word_file_name)
        chunk.export(output_path, format="wav")
        word_files.append(output_path)



    return word_files


def save_audio(file):
    file_path = os.path.join("uploads", file.filename)
    try:
        file.save(file_path)
        return file_path, True
    except Exception as e:
        print(f"Failed to save file: {e}")
        return None, False


# def convert_m4a_to_wav(m4a_file_path):
#     if os.path.exists(m4a_file_path):
#         wav_file_path = m4a_file_path.replace(".m4a", ".wav")
#         try:
#             audio = AudioSegment.from_file(m4a_file_path, format="m4a")
#             # Export the audio to WAV format
#             audio.export(wav_file_path, format="wav")
#             # remove m4a file
#             os.remove(m4a_file_path)
#             return wav_file_path
#         except Exception as e:
#             print(f"Failed to convert file: {e}")
#             return None
#     else:
#         print(f"m4a  not found at {m4a_file_path}")
#         return None


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


def spechToTextOnline(wav_file_path):

    if not os.path.exists(wav_file_path):
        return "Command not exist"

    # Load audio with librosa
    # audio_data, sr_rate = librosa.load(wav_file_path, sr=None)
    # Convert audio to text using SpeechRecognition

    recognizer = sr.Recognizer()
    audio = sr.AudioFile(wav_file_path)

    with audio as source:
        audio_content = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_content)
        print(text)
    except sr.UnknownValueError:
        # text = "Could not understand audio"
        text = ""
    except sr.RequestError as e:
        text = f"Could not request results; {e}"

    return text

def processVoiceCommand(wav_file_path):
    audio_segment = loadAudio(wav_file_path)
    print(f"Duration of the origional audio: {len(audio_segment)} ms")
    # remove last and start noise
    trimmed_audio = cleanAudioFromStartandEnd(audio_segment, silence_thresh=-34.3, chunk_size=10) # silence_thresh=-28, chunk_size=10
    # split audio into list of words audio
    commands = split_audio_on_silence(trimmed_audio, min_silence_len=80, silence_thresh=-50) # min_silence_len=80, silence_thresh=-50
    print("Split audio files:", commands)


    # clean audios
    if len(commands) > 1:
        filtered_commands = [commands[0], commands[-1]]
    else:
        filtered_commands = commands


    print("filtered commands :",filtered_commands)



    ############### Do Next Work below Here #########################################
    # Load the pre-trained model
    model = tf.keras.models.load_model(model_path)
    # Rough Work
    text = []
    for command in filtered_commands:
        print("Commad inside loop :",command)
        features = extract_features(command)

        # Reshape the features to match the model's expected input shape
        features = np.reshape(features, (1, 1408, 1))  # (batch_size=1, 1408, 1)

        print("Reshaped featureas  ",features)

        # Predict using the model
        result = model.predict(features)
        predicted_index = int(np.argmax(result))

        print("Predicted index :",predicted_index)

        reverse_labels_dict = {v: k for k, v in labels_dict.items()}
        predicted_label = reverse_labels_dict.get(predicted_index, 'Label not found')
        print("Predicted label :", predicted_label)
        text.append(predicted_label)

    # text = []
    # for command in filtered_commands:
    #     text.append(spechToTextOnline(command))



    ############### Do Next Work above this #########################################

    # remove converted wav file
    if os.path.exists(wav_file_path):
        os.remove(wav_file_path)

    print("List of labels:  ",text)
    return text
