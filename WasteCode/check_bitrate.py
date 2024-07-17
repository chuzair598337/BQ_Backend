import os

from pydub import AudioSegment

def get_audio_bitrate(file_path):
    audio = AudioSegment.from_file(file_path)
    bitrate = audio.frame_rate * audio.frame_width * 8  # frame_rate in Hz, frame_width in bytes
    return bitrate


def main(input_folder):
    # Ensure input folder exists
    if not os.path.exists(input_folder):
        print(f"Error[0] : {input_folder} directory not found...")
        return

    # Check if input folder is empty
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.m4a')]
    if not input_files:
        print(f"Error[0] : {input_folder} is empty")
        return

    for i,file in enumerate(input_files):
        bitrate = get_audio_bitrate(file)
        print(f'Bitrate[{i+1}]: {bitrate} bps')

if __name__ == "__main__":
    input_folder = 'Dataset'
    main(input_folder)