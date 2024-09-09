import os
from pydub import AudioSegment
from flask import jsonify
import librosa
import speech_recognition as sr
import shutil
from pydub.silence import split_on_silence, detect_leading_silence


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


def convert_m4a_to_wav(m4a_file_path):
    if os.path.exists(m4a_file_path):
        wav_file_path = m4a_file_path.replace(".m4a", ".wav")
        try:
            audio = AudioSegment.from_file(m4a_file_path, format="m4a")
            # Export the audio to WAV format
            audio.export(wav_file_path, format="wav")
            # remove m4a file
            os.remove(m4a_file_path)
            return wav_file_path
        except Exception as e:
            print(f"Failed to convert file: {e}")
            return None
    else:
        print(f"m4a  not found at {m4a_file_path}")
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





    ############### Do Next Work below Here #########################################

    # Rough Work
    text = []
    for command in filtered_commands:
        text.append(spechToTextOnline(command))

    ############### Do  Next Work above this #########################################

    # remove converted wav file
    if os.path.exists(wav_file_path):
        os.remove(wav_file_path)

    return text
