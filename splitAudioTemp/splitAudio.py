import os
import shutil

from pydub import AudioSegment
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


if __name__ == "__main__":
    #currentFilePath = os.path.dirname(__file__)
    #audio_folder = os.path.join(currentFilePath,"audio")
   # Example usage
    #audio_path = f"{audio_folder}/sample_play_yaseen.wav"
    audio_path = f"recording.wav"
    audio_segment = loadAudio(audio_path)
    print(f"Duration of the origional audio: {len(audio_segment)} ms")
    # remove last and start noise
    trimmed_audio = cleanAudioFromStartandEnd(audio_segment,silence_thresh=-34.3,chunk_size=10)
    word_files = split_audio_on_silence(trimmed_audio,min_silence_len=1000, silence_thresh=-16)
    print("Split audio files:", word_files)
