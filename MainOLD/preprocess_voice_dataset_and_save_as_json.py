# import some libraries for preprocessing
import librosa
import os
import json

currentFilePath = os.path.dirname(__file__)
DATASET_PATH = os.path.join(currentFilePath,'..','Dataset')
modalDir = os.path.join(currentFilePath,'Model_data')
JSON_DATA_FILE = os.path.join(modalDir,"Preprocess_Json_file4.json")
SAMPLE_TO_CONSIDER = 22050
print(currentFilePath)
print(DATASET_PATH)
print(JSON_DATA_FILE)
print()

def pre_process_dataSet(dataset_path, json_dat_file, n_mfcc=13, hop_length=512, n_fft=2048):

    # 1 : data Dictionary for records
    data = {
        "mappings": [],
        "labels": [],
        "MFCCs": [],
        "files": []
    }

    # 2: loop through all subdirectories
    for i, (dirpath, dirname, filenames) in enumerate(os.walk(dataset_path)):

        # check weather we are not in root path
        if dirpath is not dataset_path:

            category = dirpath.split("/")[-1]
            print()
            data["mappings"].append(category)
            print(f"processing:{category}")

            for f in filenames:


                file_path = os.path.join(dirpath, f)   #data1/down/down1.wav
                signal, sr = librosa.load(path=file_path, mono=True)

                if len(signal) >= SAMPLE_TO_CONSIDER:

                    signal = signal[:SAMPLE_TO_CONSIDER]

                    MFCCs = librosa.feature.mfcc(y=signal, n_mfcc=n_mfcc, hop_length=hop_length, n_fft=n_fft)

                    # Stored Data in Dictionary
                    data["labels"].append(i-1)
                    data["MFCCs"].append(MFCCs.T.tolist())
                    data["files"].append(file_path)
                    print(f"{file_path}:{i-1}")

    with open(json_dat_file, 'w') as fp:
        json.dump(data, fp, indent=4)


if __name__ == "__main__":
    #pre_process_dataSet(DATASET_PATH, JSON_DATA_FILE)
    print('done')


