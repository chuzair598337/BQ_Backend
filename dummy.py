import numpy as np
import librosa

# Load the audio file
audio_path = 'D:\\GitHub\\BQ_Backend\\Audio_Voices\\suras\\Aal-E-Imran\\AUDIO-2024-07-14-23-07-17 2.wav'  # Replace with your audio file path
y, sr = librosa.load(audio_path, sr=None)

# Extract MFCCs (Mel-frequency cepstral coefficients)
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

# Extract Chroma features
chroma = librosa.feature.chroma_stft(y=y, sr=sr)

# Extract Spectral Contrast
spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

# Flatten the features into a single array (optional)
features = np.concatenate((mfccs.flatten(), chroma.flatten(), spectral_contrast.flatten()))

print("Extracted Features Shape:", features.shape)
print("Extracted Features:", features)