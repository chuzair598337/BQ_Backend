from FlaskApi.MakeCSV_code import features

# Desired number of samples for resampling
target_samples = 22050


labels_dict = {
    'Al-Falaq': 0, 'Al-Fatiha': 1, 'Al-Ikhlas': 2, 'An-Nas': 3, 'Ar-Rahman': 4,'Maryam':5,'Muhammad':6,
    'Next':7,'Pause':8,'Play':9,'Previous':10,'Ya-Sin':11,'Yusuf':12,'Al-Kafirun':13,'GoTo':14,'Repeat':15
}

# Folder for Storing Model data
data_Folder = "Data"

# Model File Name
ModelName = "STT_Model.keras"

# CSV File Name
featuresFile = "features.csv"

# Posted Audio Files
ApiUpload = "uploads"
