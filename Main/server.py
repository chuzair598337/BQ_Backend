import os
from flask import Flask, request, jsonify
import random
from pydub import AudioSegment
from prediction_key_words import Keyword_Spotting_Service


class Prediction:
    def __init__(self, predicted_keyword, options, input_audio_mffc):
        self.predicted_keyword = predicted_keyword
        self.options = options
        self.input_audio_mffc = input_audio_mffc


app = Flask(__name__)
@app.route("/predict", methods=["POST"])
def predict():

    # get file and Save
    audio_file = request.files['file']
    file_name = 'audio.wav'
    audio_file.save(file_name)

    # invoke keyword_services
    kss = Keyword_Spotting_Service()
    print(" KSS ",kss)
    # make prediction
    keyword, options, mffc = kss.predict(file_name)
    os.remove(file_name)
    val = ""
    for v in keyword:
        val=val+v+" "
    res = Prediction(predicted_keyword=val, options=options,input_audio_mffc= mffc)
    return jsonify({
        'predicted_keyword':res.predicted_keyword,
        'options':res.options,
        'input_audio_mffc' : res.input_audio_mffc
    })


if __name__ == "__main__":
    app.run(host="", port=4444)
