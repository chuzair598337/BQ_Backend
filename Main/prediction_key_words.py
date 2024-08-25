import os
import librosa
import tensorflow as tf
import numpy as np
# import record_from_mic as rc
from pydub import AudioSegment
from pydub import silence
import tempfile

temp_files = []

SAVED_MODEL_PATH = "Model_data/model4.h5"
TEST_DATASET_PATH = "test_data/data/"
SAMPLES_TO_CONSIDER = 22050

class _Keyword_Spotting_Service:
    """Singleton class for keyword spotting inference with trained models.
    :param model: Trained model
    """

    model = None
    _mapping = [
        "Al-Baqarah",
        "Al-Falaq",
        "Al-Fatihah",
        "Al-Ikhlas",
        "An-Nas",
        "Bayan",
        "BookMark",
        "end_aytno",
        "home",
        "menu",
        "mode",
        "next",
        "Pause",
        "play",
        "prevoius",
        "repeat",
        "settings",
        "stop",
        "st_aytno",
        "tafheem",
        "tilawat"
    ]
    _instance = None

    def get_audio_split(self,filepath):
        spliti = filepath.split('.')
        audio_file = AudioSegment.from_file(filepath)
        split_length = 1000
        duration = len(audio_file)
        num_splits = duration // split_length
        audios = []
        # Define the start and end time for each split
        split_start_times = [i * split_length for i in range(num_splits)]
        split_end_times = [(i + 1) * split_length for i in range(num_splits)]
        if len(split_end_times) == 0:
            print('nothing')
        else:
            split_end_times[-1] = duration  # Set the end time of the last split segment to the end of the audio file
        for i in range(num_splits):
            # Extract the audio segment using the start and end time
            segment = audio_file[split_start_times[i]:split_end_times[i]]
            # Export the audio segment as a new file
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            # Export the audio segment to the temporary file
            segment.export(temp_file.name, format='wav')
            temp_files.append(temp_file.name)

    def predict(self, file_path):

        # extract MFCC
        MFCCs = self.preprocess(file_path)
        predicted_words = []
        multioption=[]
        itrator = 0
        multiflag = False
        input_audio_mffc = ''
        # we need a 4-dim array to feed to the model for prediction: (# samples, # time steps, # coefficients, 1)
        for mffc in MFCCs:
            mffc = mffc[np.newaxis, ..., np.newaxis]

            resized_input_data = np.zeros((mffc.shape[0], 44, mffc.shape[2], 1))
            for i in range(mffc.shape[0]):
                resized_input_data[i, :, :, :] = np.resize(mffc[i, :, :, :], (44, mffc.shape[2], 1))

            # get the predicted label
            predictions = self.model.predict(resized_input_data)
            predicted_index = np.argmax(predictions)
            print(predicted_index)
            predicted_keyword = self._mapping[predicted_index]
            predicted_words.append(predicted_keyword)


            if multiflag == True and itrator==1 and self.check_weather_word_is_general_or_not(predicted_keyword)==True:
                arr = np.array(predictions)
                sorted_index = np.argsort(arr)
                sorted_index = sorted(sorted_index)
                multioption.append(self._mapping[sorted_index[-1][-1]])
                multioption.append(self._mapping[sorted_index[-1][-2]])
                multioption.append(self._mapping[sorted_index[-1][-3]])
                input_audio_mffc = str(resized_input_data)
                itrator+=1

            if predicted_keyword == 'play':
                multiflag = True
                itrator=1
        print('after ', predicted_words)
        return predicted_words, multioption,input_audio_mffc

    def check_weather_word_is_general_or_not(self, words):
        general_words = ["Al-Baqarah","Al-Falaq","Al-Fatihah","Al-Ikhlas","An-Nas","Bayan","tafheem","tilawat"]
        if general_words.__contains__(words):
            return True
        else:
            return  False

    def preprocess(self, file_path, num_mfcc=13, n_fft=2048, hop_length=512):

        # Load the audio file
        mffc_transfos = []
        for file in temp_files:
            os.remove(file)
            temp_files.remove(file)
        self.get_audio_split(file_path)
        # Export each chunk to a new file

        for temp in enumerate(temp_files):
            print(temp[1])
            signal, sample_rate = librosa.load(path=temp[1], sr=SAMPLES_TO_CONSIDER, mono=True)

            if len(signal) >= SAMPLES_TO_CONSIDER:
                # ensure consistency of the length of the signal
                signal = signal[:SAMPLES_TO_CONSIDER]

            # extract MFCCs
            MFCCs = librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=num_mfcc, n_fft=n_fft,hop_length=hop_length)
            mffc_transfos.append(MFCCs.T)
        # load audio file
        for file in temp_files:
            os.remove(file)
            temp_files.remove(file)
        return mffc_transfos


def Keyword_Spotting_Service():
    # ensure an instance is created only the first time the factory function is called
    if _Keyword_Spotting_Service._instance is None:
        _Keyword_Spotting_Service._instance = _Keyword_Spotting_Service()
        _Keyword_Spotting_Service.model = tf.keras.models.load_model(SAVED_MODEL_PATH)
    return _Keyword_Spotting_Service._instance


if __name__ == "__main__":
    kss = Keyword_Spotting_Service()
    print(kss.predict(f"C:/Users/azaz/Downloads/new1.ogg"))
    # print(kss.predict(f"{TEST_DATASET_PATH}mix.aac"))