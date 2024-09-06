import os

from pydub import AudioSegment
from pydub.silence import split_on_silence


def split_audio_on_silence(audio_path):
    # Load the audio file
    audio = AudioSegment.from_wav(audio_path)

    # Split audio where the silence is longer than 500ms and silence is quieter than -40dB
    chunks = split_on_silence(
        audio,
        min_silence_len=500,
        silence_thresh=-40
    )

    word_files = []

    # Export each chunk as a separate file
    for i, chunk in enumerate(chunks):
        word_file_name = f"command_{i + 1}.wav"
        chunk.export(word_file_name, format="wav")
        word_files.append(word_file_name)

    return word_files


if __name__ == "__main__":
    currentFilePath = os.path.dirname(__file__)
    audio_folder = os.path.join(currentFilePath,"audio")
   # Example usage
    audio_path = f"{audio_folder}/input.wav"
    word_files = split_audio_on_silence(audio_path)

    print("Split audio files:", word_files)
