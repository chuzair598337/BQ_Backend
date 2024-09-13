import os
import numpy as np
import librosa
import tensorflow as tf
from flask import Flask, request, jsonify
from globalVariables import *
from sklearn.preprocessing import StandardScaler
import pickle


app = Flask(__name__)

# Paths to your model and scaler
currentFilePath = os.path.dirname(__file__)
model_path = os.path.join(currentFilePath, data_Folder, ModelName)

# Load the trained model and scaler
model = tf.keras.models.load_model(model_path)

# Desired number of samples for resampling
target_samples = 22050  # Example target number of samples


def preprocess_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)

    # Resample the audio to the target number of samples
    if len(y) != target_samples:
        y = librosa.resample(y, orig_sr=sr, target_sr=target_samples * sr // len(y))

    # Extract MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=target_samples, n_mfcc=13)

    # Extract Chroma features
    chroma = librosa.feature.chroma_stft(y=y, sr=target_samples)

    # Extract Spectral Contrast
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=target_samples)

    # Flatten the features into a single array
    features = np.concatenate((mfccs.flatten(), chroma.flatten(), spectral_contrast.flatten()))

    # Reshape to match the input shape of the model
    features = features.reshape(1, -1)

    # with open(scaler_path, 'rb') as f:
    #     scaler = pickle.load(f)
    #     print(type(scaler))  # Make sure this prints the expected scaler type
    #
    # # Ensure scaler is indeed a StandardScaler or similar instance
    # if isinstance(scaler, StandardScaler):
    #     # Proceed with transform
    #     features = scaler.transform(features)
    # else:
    #     raise TypeError("Loaded scaler is not a valid StandardScaler instance.")
    #
    # # Normalize the features using the loaded scaler
    # features = scaler.transform(features)

    # Reshape to fit the model's expected input shape
    features = features.reshape(1, features.shape[1], 1)

    return features


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file:
        # Save the uploaded file temporarily
        temp_path = os.path.join(currentFilePath, 'temp_audio.wav')
        file.save(temp_path)

        # Preprocess the audio file
        features = preprocess_audio(temp_path)

        # Predict the class
        predictions = model.predict(features)
        predicted_label = np.argmax(predictions, axis=1)[0]
        predicted_class = labels_dict[predicted_label]

        # Remove the temporary file
        os.remove(temp_path)

        return jsonify({"prediction": predicted_class}), 200

    return jsonify({"error": "File processing failed"}), 500


if __name__ == '__main__':
    app.run(debug=True)
