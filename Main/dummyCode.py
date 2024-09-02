import os
import numpy as np
import librosa
import csv

labels_dict = {
    'Al-Fatiha': 0, 'Al-Baqarah': 1, 'Aal-E-Imran': 2, 'An-Nisa': 3, 'Al-Maidah': 4, 'Al-Anam': 5,
    'Al-Araf': 6, 'Al-Anfal': 7, 'At-Tawbah': 8, 'Yunus': 9, 'Hud': 10, 'Yusuf': 11, 'Ar-Rad': 12, 'Ibrahim': 13,
    'Al-Hijr': 14, 'An-Nahl': 15, 'Al-Isra': 16, 'Al-Kahf': 17, 'Maryam': 18, 'Ta-Ha': 19, 'Al-Anbiya': 20,
    'Al-Hajj': 21, 'Al-Muminun': 22, 'An-Nur': 23, 'Al-Furqan': 24, 'Ash-Shuara': 25, 'An-Naml': 26, 'Al-Qasas': 27,
    'Al-Ankabut': 28, 'Ar-Rum': 29, 'Luqman': 30, 'As-Sajda': 31, 'Al-Ahzab': 32, 'Saba': 33, 'Fatir': 34, 'Ya-Sin': 35,
    'As-Saffat': 36, 'Sad': 37, 'Az-Zumar': 38, 'Al-Mumin': 39, 'Fussilat': 40, 'Ash-Shura': 41, 'Az-Zukhruf': 42,
    'Ad-Dukhan': 43, 'Al-Jathiya': 44, 'Al-Ahqaf': 45, 'Muhammad': 46, 'Al-Fath': 47, 'Al-Hujraat': 48, 'Qaf': 49,
    'Adh-Dhariyat': 50, 'At-Tur': 51, 'An-Najm': 52, 'Al-Qamar': 53, 'Ar-Rahman': 54, 'Al-Waqia': 55, 'Al-Hadid': 56,
    'Al-Mujadila': 57, 'Al-Hashr': 58, 'Al-Mumtahina': 59, 'As-Saff': 60, 'Al-Jumua': 61, 'Al-Munafiqun': 62,
    'At-Taghabun': 63, 'At-Talaq': 64, 'At-Tahrim': 65, 'Al-Mulk': 66, 'Al-Qalam': 67, 'Al-Haaqqa': 68,
    'Al-Maarij': 69, 'Nuh': 70, 'Al-Jinn': 71, 'Al-Muzzammil': 72, 'Al-Muddathir': 73, 'Al-Qiyama': 74,
    'Al-Insan': 75, 'Al-Mursalat': 76, 'An-Naba': 77, 'An-Naziat': 78, 'Abasa': 79, 'At-Takwir': 80, 'Al-Infitar': 81,
    'Al-Mutaffifin': 82, 'Al-Inshiqaq': 83, 'Al-Burooj': 84, 'At-Tariq': 85, 'Al-Ala': 86, 'Al-Ghashiya': 87,
    'Al-Fajr': 88, 'Al-Balad': 89, 'Ash-Shams': 90, 'Al-Lail': 91, 'Ad-Duhaa': 92, 'Ash-Sharh': 93, 'At-Tin': 94,
    'Al-Alaq': 95, 'Al-Qadr': 96, 'Al-Bayyina': 97, 'Az-Zalzala': 98, 'Al-Adiyat': 99, 'Al-Qaria': 100, 'At-Takathur': 101,
    'Al-Asr': 102, 'Al-Humaza': 103, 'Al-Fil': 104, 'Quraish': 105, 'Al-Maun': 106, 'Al-Kawthar': 107, 'Al-Kafiroon': 108,
    'An-Nasr': 109, 'Al-Masad': 110, 'Al-Ikhlas': 111, 'Al-Falaq': 112, 'An-Nas': 113
}

# Define the target length for feature arrays
target_length = 1000  # This can be adjusted based on your needs

# Create a single CSV file for all data
output_file = 'combined_data.csv'
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

                    # Extract MFCCs (Mel-frequency cepstral coefficients)
                    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

                    # Extract Chroma features
                    chroma = librosa.feature.chroma_stft(y=y, sr=sr)

                    # Extract Spectral Contrast
                    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

                    # Flatten the features into a single array
                    features = np.concatenate((mfccs.flatten(), chroma.flatten(), spectral_contrast.flatten()))

                    # Pad or truncate features to the target length
                    if len(features) < target_length:
                        features = np.pad(features, (0, target_length - len(features)), mode='constant')
                    else:
                        features = features[:target_length]

                    # Create a record with the label and features
                    record = [label] + features.tolist()

                    # Write the record to the CSV file
                    writer.writerow(record)