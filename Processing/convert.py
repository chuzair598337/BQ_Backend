import os
from pydub import AudioSegment
import shutil
from datetime import datetime


def convert_m4a_to_wav(input_file, output_file):
    try:
        audio = AudioSegment.from_file(input_file, format="m4a")
        audio.export(output_file, format="wav")
        return True
    except Exception as e:
        print(f"Error converting {input_file}: {e}")
        return False


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def main(input_folder, output_folder, success_folder, failure_folder,isInRoot):

    if not isInRoot:
        input_folder = os.path.join(input_folder,'..')




    # Ensure input_folder exists
    if not os.path.exists(input_folder):
        print(f"Error: {input_folder} directory not found...")
        return

    # Ensure directories exist
    ensure_directory_exists(output_folder)
    ensure_directory_exists(success_folder)
    ensure_directory_exists(failure_folder)

    # Check if input folder is empty
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.m4a')]
    if not input_files:
        print(f"{input_folder} is empty")
        return

    total_files = len(input_files)
    processed_files = 0
    success_files = 0
    failed_files = 0
    warningsCounter = 0

    for file in input_files:
        input_file_path = os.path.join(input_folder, file)
        output_file_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".wav")
        sucess_file_path = os.path.join(success_folder, file)
        timestamped_failure_folder = os.path.join(failure_folder, datetime.now().strftime('%Y%m%d%H%M%S'))

        if os.path.exists(output_file_path):
            warningsCounter += 1
            print(f"\t Warning[{warningsCounter}] : {file} already Exist in {output_folder} ...")
            continue

        if convert_m4a_to_wav(input_file_path, output_file_path):
            if os.path.exists(sucess_file_path):
                warningsCounter += 1
                print(f"\t Warning[{warningsCounter}] : {file} already Exist in {success_folder} ...")
                continue
            shutil.move(input_file_path, success_folder)
            success_files += 1
        else:
            ensure_directory_exists(timestamped_failure_folder)
            shutil.move(input_file_path, timestamped_failure_folder)
            failed_files += 1

        processed_files += 1
        progress_percentage = (processed_files / total_files) * 100
        success_percentage = (success_files / total_files) * 100
        failed_percentage = (failed_files / total_files) * 100

        print(f"Processed {processed_files}/{total_files} ({progress_percentage:.2f}%) "
              f"### Success {success_files}/{total_files} ({success_percentage:.2f}%) "
              f"# Failure {failed_files}/{total_files} ({failed_percentage:.2f}%)")


if __name__ == "__main__":
    input_folder = "Dataset"
    output_folder = "Dataset_Converted"
    failure_folder = "failureConversion"
    success_folder = "successConversion"
    isInRoot = False

    #main(input_folder, output_folder, success_folder, failure_folder,isInRoot)

    import os

    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    #print(current_directory)

    # Assuming the script is in a subdirectory within the project, navigate up
    project_root = os.path.abspath(os.path.join(current_directory, '..'))
    #print("Project Root:", project_root)

    a = os.path.join(input_folder,'..','..')
    print(os.path.abspath(a))



