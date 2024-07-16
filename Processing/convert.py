import os
from pydub import AudioSegment
import shutil
from datetime import datetime


def convert_m4a_to_wav(input_file_path, output_file_path):
    try:
        audio = AudioSegment.from_file(input_file_path, format="m4a")
        audio.export(output_file_path, format="wav")
        return True,""
    except Exception as e:
        return False,e


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def main(input_folder, output_folder, success_folder, failure_folder):


    processed_files = 0
    success_files = 0
    failed_files = 0
    warning_files = 0
    errorCounter = 0

    # Ensure input_folder exists
    if not os.path.exists(input_folder):
        errorCounter += 1
        print(f"Error[{failed_files}] : {input_folder} directory not found...")
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

    for file in input_files:
        input_file_path = os.path.join(input_folder, file)
        output_file_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".wav")
        sucess_file_path = os.path.join(success_folder, file)
        timestamped_failure_folder = os.path.join(failure_folder, datetime.now().strftime('%Y%m%d%H%M%S'))

        if os.path.exists(output_file_path):
            warning_files += 1
            print(f"\t Warning[{warning_files}] : {file} already Exist in {output_folder} ...")
            processed_files = execute_log(processed_files, success_files, failed_files,warning_files,total_files)
            continue

        result,error = convert_m4a_to_wav(input_file_path, output_file_path)
        if result:
            if os.path.exists(sucess_file_path):
                warning_files += 1
                print(f"\t Warning[{warning_files}] : {file} already Exist in {success_folder} ...")
                processed_files = execute_log(processed_files, success_files, failed_files,warning_files,total_files)
                continue

            shutil.move(input_file_path, success_folder)
            success_files += 1
        else:
            failed_files += 1
            print(f"Error[{failed_files}] : converting {input_file_path} : \n {error}")
            ensure_directory_exists(timestamped_failure_folder)
            shutil.move(input_file_path, timestamped_failure_folder)


        processed_files = execute_log(processed_files, success_files, failed_files,warning_files,total_files)




def execute_log(processed_files, success_files, failed_files,warning_files,total_files):
    processed_files += 1
    progress_percentage = (processed_files / total_files) * 100
    success_percentage = (success_files / total_files) * 100
    failed_percentage = (failed_files / total_files) * 100
    warnings_percentage = (warning_files / total_files) * 100

    print(f"Processed {processed_files}/{total_files} ({progress_percentage:.2f}%) ===> [ "
          f" Success {success_files}/{total_files} ({success_percentage:.2f}%) "
          f" ### Failure {failed_files}/{total_files} ({failed_percentage:.2f}%)"
          f" ### Warnings {warning_files}/{total_files} ({warnings_percentage:.2f}%) ]")

    return processed_files



if __name__ == "__main__":
    input_folder = "Dataset"
    output_folder = "Dataset_Converted"
    failure_folder = "failureConversion"
    success_folder = "successConversion"

    main(input_folder, output_folder, success_folder, failure_folder)



