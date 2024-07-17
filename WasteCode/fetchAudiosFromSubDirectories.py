import os
import shutil

dataset_path = "Dataset_Origonal"
output_folder = "AllVoices"
count_copied_files = 0

# Walk through all subdirectories and files
for dirpath, dirnames, filenames in os.walk(dataset_path):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        shutil.copy(file_path, output_folder)
        count_copied_files += 1

print(f"Total {count_copied_files} files copied to {output_folder}.")
