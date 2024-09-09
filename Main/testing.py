import os
import numpy as np
import librosa
import csv

labels_dict = {
    'Al-Falaq': 0, 'Al-Fatiha': 1, 'Al-Ikhlas': 2, 'An-Nas': 3, 'Ar-Rahman': 4,'Maryam':5,'Muhammad':6,
    'Next':7,'Pause':8,'Play':9,'Previous':10,'Ya-Sin':11,'Yusuf':12
}

# Desired number of samples for resampling
target_samples = 22050  # Example target number of samples
# Create a single CSV file for all data
output_file = 'combined_data_resampled.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Loop over each Surah label
    for surah, label in labels_dict.items():
        # Construct the path to the folder containing the audio files for the current Surah
        path = os.path.join('D:\\GitHub\\BQ_Backend\\Audio_Voices\\Suras', surah)

        # Walk through the directory structure
        for root, dirs, files in os.walk(path):
            for filename in files:
                if filename.endswith('.wav'):
                    # Prepare to process each .wav file
                    file_path = os.path.join(root, filename)
                    y, sr = librosa.load(file_path, sr=None)

                    # Resample the audio to the target number of samples
                    if len(y) != target_samples:
                        y = librosa.resample(y, orig_sr=sr, target_sr=target_samples * sr // len(y))

                    # Extract MFCCs (Mel-frequency cepstral coefficients)
                    mfccs = librosa.feature.mfcc(y=y, sr=target_samples, n_mfcc=13)

                    # Extract Chroma features
                    chroma = librosa.feature.chroma_stft(y=y, sr=target_samples)

                    # Extract Spectral Contrast
                    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=target_samples)

                    # Flatten the features into a single array
                    features = np.concatenate((mfccs.flatten(), chroma.flatten(), spectral_contrast.flatten()))

                    # Create a record with the label and features
                    record = [label] + features.tolist()

                    # Write the record to the CSV file
                    writer.writerow(record)