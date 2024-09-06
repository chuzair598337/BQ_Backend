from flask import Flask, request, jsonify
import librosa
import numpy as np
import tensorflow as tf
from Main.testing import labels_dict

SAVED_MODEL_PATH = "Mymodel1.h5"
app = Flask(__name__)

def extract_features(file_name):
    # Load the audio file using librosa
    y, sr = librosa.load(file_name, sr=None)

    # Extract features (e.g., MFCCs, Chroma, Mel spectrogram, etc.)
    # We'll extract 40 MFCCs (Mel-frequency cepstral coefficients)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)

    # Flatten the MFCCs to create a single feature vector
    mfccs_scaled = np.mean(mfccs.T, axis=0)

    # Ensure we have 1408 features by resizing or padding
    feature_vector = np.resize(mfccs_scaled, (1408,))

    return feature_vector

@app.route("/predict", methods=["POST"])
def predict():
    # Get the audio file from the request
    audio_file = request.files['file']
    file_name = 'audio.wav'

    # Save the file locally
    audio_file.save(file_name)

    # Extract features from the saved audio file
    features = extract_features(file_name)

    # Load the pre-trained model
    model = tf.keras.models.load_model(SAVED_MODEL_PATH)

    # Reshape the features to match the model's expected input shape
    features = np.reshape(features, (1, 1408, 1))  # (batch_size=1, 1408, 1)

    # Predict using the model
    result = model.predict(features)
    predicted_index = int(np.argmax(result))
    print(predicted_index)
    # predicted_value=labels_dict[predicted_index]
    reverse_labels_dict = {v: k for k, v in labels_dict.items()}
    predicted_label = reverse_labels_dict.get(predicted_index, 'Label not found')
    # Return the prediction as a response
    return jsonify({"predicted value ": predicted_label})

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
