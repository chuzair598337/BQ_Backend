import os
import shutil

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

currentFilePath = os.path.dirname(__file__)
output_folder = os.path.join(currentFilePath,'..',"NewAllVoices")
ensure_directory_exists(output_folder)
dataset_path = "Dataset"
count_copied_files = 0


# Walk through all subdirectories and files
for dirpath, dirnames, filenames in os.walk(dataset_path):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        shutil.copy(file_path, output_folder)
        count_copied_files += 1

print(f"Total {count_copied_files} files copied to {output_folder}.")
