import os
import glob
import librosa
import numpy as np
from scipy.fftpack import fft

def calculate_spectral_centroid(audio, sr,n_fft=512):
    """Calculate the spectral centroid of the audio."""
    # Calculate the Short-Time Fourier Transform (STFT) of the audio
    stft = np.abs(librosa.stft(audio,n_fft=n_fft))
    # Calculate the spectral centroid
    spectral_centroid = librosa.feature.spectral_centroid(S=stft, sr=sr)
    # Average spectral centroid
    return np.mean(spectral_centroid)

def is_significant_audio(file_path, threshold_centroid):
    """Check if audio file's spectral centroid is above the threshold."""
    audio, sr = librosa.load(file_path, sr=None)
    # Calculate spectral centroid of the audio
    centroid = calculate_spectral_centroid(audio, sr)
    return centroid > threshold_centroid

def filter_audios(directory, threshold_centroid):
    """Filter audio files based on spectral centroid threshold."""
    audio_files = glob.glob(os.path.join(directory, '*.wav'))
    filtered_files = []

    for file in audio_files:
        if is_significant_audio(file, threshold_centroid):
            filtered_files.append(file)
            print(f"File '{file}' is considered significant.")
        else:
            print(f"File '{file}' is considered noise or insignificant.")

    return filtered_files


if __name__ == '__main__':
    # Define the directory and threshold
    directory = 'output'
    threshold_centroid = 1350

    # Filter audios
    filtered_audios = filter_audios(directory, threshold_centroid)

    # Optional: Remove files that are considered noise
    for file in glob.glob(os.path.join(directory, '*.wav')):
        if file not in filtered_audios:
            os.remove(file)
            print(f"Removed file '{file}'.")
