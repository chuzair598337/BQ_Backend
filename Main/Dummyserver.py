from flask import Flask, request, jsonify
import librosa
import numpy as np
import tensorflow as tf

from Main.testing import labels_dict

SAVED_MODEL_PATH = "Mymodel1.h5"
app = Flask(__name__)

# New feature extraction function with segmentation
def extract_features_segmented(file_name, segment_duration=2.0):
    y, sr = librosa.load(file_name, sr=None)

    # Segment the audio into chunks (e.g., 2 seconds per chunk)
    total_duration = librosa.get_duration(y=y, sr=sr)
    num_segments = int(total_duration // segment_duration)
    feature_list = []

    for i in range(num_segments):
        start = int(i * segment_duration * sr)
        end = int((i + 1) * segment_duration * sr)
        y_segment = y[start:end]

        # Extract features for each segment
        mfccs = librosa.feature.mfcc(y=y_segment, sr=sr, n_mfcc=40)
        mfccs_scaled = np.mean(mfccs.T, axis=0)
        feature_list.append(mfccs_scaled)

    return np.array(feature_list)

@app.route("/predict", methods=["POST"])
def predict():
    # Get the audio file from the request
    audio_file = request.files['file']
    file_name = 'audio.wav'

    # Save the file locally
    audio_file.save(file_name)

    # Extract features from the saved audio file (using segmented approach)
    features_segments = extract_features_segmented(file_name)
    print(features_segments)

    # Load the pre-trained model
    model = tf.keras.models.load_model(SAVED_MODEL_PATH)

    # Make predictions for each audio segment
    predictions = []
    for features in features_segments:
        features = np.reshape(features, (1, 40, 1))  # Reshape to match the model input shape
        result = model.predict(features)
        predicted_index = int(np.argmax(result))
        predictions.append(predicted_index)

    # Convert the predicted indices to labels
    reverse_labels_dict = {v: k for k, v in labels_dict.items()}
    predicted_labels = [reverse_labels_dict.get(index, 'Label not found') for index in predictions]

    # Create a coherent command based on the predicted labels
    # Join the unique labels while maintaining their order
    unique_labels = list(dict.fromkeys(predicted_labels))

    # Combine labels into a single command string
    predicted_command = " ".join(unique_labels).strip()

    # Return the prediction as a response
    return jsonify({"predicted value": predicted_command})


if __name__ == "__main__":
    app.run(debug=True)
