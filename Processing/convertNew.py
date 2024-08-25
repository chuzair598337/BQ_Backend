import os
import time

from pydub import AudioSegment
import shutil
from datetime import datetime

def delete_empty_directory(directory_path):
    try:
        os.rmdir(directory_path)
    except OSError as e:
        print(f"Error[?]: {directory_path} : {e.strerror}")

def convert_m4a_to_wav(input_file_path, output_file_path):
    isTrimmed = False
    try:
        audio = AudioSegment.from_file(input_file_path, format="m4a")
        print(len(audio))
        if len(audio) > 2000:
            # Trim audio to approximately 1 second
            new_audio = audio[-1600:-100]  # Trim last 1 second (1000 milliseconds)
            isTrimmed = True
        else:
            new_audio = audio
        # Export the trimmed audio to WAV format
        new_audio.export(output_file_path, format="wav")
        return True,isTrimmed, ""
    except Exception as e:
        return False,isTrimmed, str(e)


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def log_progress(processed_files, success_files, failed_files, warning_files, files_to_process,trimmed_count):
    progress_percentage = (processed_files / files_to_process) * 100
    success_percentage = (success_files / files_to_process) * 100
    failed_percentage = (failed_files / files_to_process) * 100
    warnings_percentage = (warning_files / files_to_process) * 100


    print(f"Processed {processed_files} ({progress_percentage:.2f}%) ===> [ "
          f"Success {success_files} ({success_percentage:.2f}%) "
          f"### Failure {failed_files} ({failed_percentage:.2f}%) "
          f"### Warnings {warning_files} ({warnings_percentage:.2f}%) "
          f"### Trimmed {trimmed_count} ]")

def main(files_to_process,files_per_set,input_folder, output_folder, success_folder, failure_folder):
    # Ensure input folder exists
    if not os.path.exists(input_folder):
        print(f"Error[0] : {input_folder} directory not found...")
        return False

    # Ensure directories exist
    ensure_directory_exists(output_folder)
    ensure_directory_exists(success_folder)
    ensure_directory_exists(failure_folder)

    # Check if input folder is empty
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.m4a')]
    if not input_files:
        print(f"Error[0] : {input_folder} is empty")
        return False

    if process_files(files_to_process,files_per_set,input_files, input_folder, output_folder, success_folder, failure_folder):
        return True

    return False

def process_files(files_to_process,files_per_set,input_files, input_folder, output_folder, success_folder, failure_folder):
    processed_files = 0
    success_files = 0
    failed_files = 0
    warning_files = 0
    trimmed_count = 0

    total_files = len(input_files)

    if files_to_process == 0:
        files_to_process = total_files
    elif files_to_process > total_files:
        print(f"Error[0] : files_to_process = {files_to_process} , total_files = {total_files}")
        print(f"Error[1] : files_to_process must be less than total_files in {output_folder} ")
        return False

    set_number = 1
    current_set_count = 0
    current_set_folder = os.path.join(output_folder, f"set{set_number}")
    ensure_directory_exists(current_set_folder)


    for i, file in enumerate(input_files):

        if i >= files_to_process:
            break

        input_file_path = os.path.join(input_folder, file)
        output_file_path = os.path.join(current_set_folder, os.path.splitext(file)[0] + ".wav")
        success_file_path = os.path.join(success_folder, file)
        timestamped_failure_folder = os.path.join(failure_folder, datetime.now().strftime('%Y%m%d%H%M%S'))

        if os.path.exists(output_file_path):
            warning_files += 1
            print(f"\tWarning[{warning_files}]: {file} already exists in {current_set_folder} ...")
            processed_files += 1
            log_progress(processed_files, success_files, failed_files, warning_files, files_to_process,trimmed_count)
            continue

        result,isTrimmed, error = convert_m4a_to_wav(input_file_path, output_file_path)
        if result:
            # if os.path.exists(success_file_path):
            #     warning_files += 1
            #     print(f"\tWarning[{warning_files}]: {file} already exists in {success_folder} ...")
            #     processed_files += 1
            #     log_progress(processed_files, success_files, failed_files, warning_files, files_to_process,trimmed_count)
            #     continue

            # .move to delete from input_folder
            # .copy to remain input_folder and copy
            # shutil.copy(str(input_file_path), str(success_folder))
            success_files += 1
        else:
            failed_files += 1
            print(f"Error[{failed_files}]: Converting {input_file_path} : \n {error}")
            ensure_directory_exists(timestamped_failure_folder)
            # .move to delete from input_folder
            # .copy to remain input_folder and copy
            shutil.copy(str(input_file_path), str(timestamped_failure_folder))

        if isTrimmed:
            trimmed_count += 1
        processed_files += 1
        current_set_count += 1

        # Check if the current set is full and create a new set folder if needed
        if current_set_count >= files_per_set and files_per_set != 0:
            set_number += 1
            current_set_count = 0
            current_set_folder = os.path.join(output_folder, f"set{set_number}")
            ensure_directory_exists(current_set_folder)

        log_progress(processed_files, success_files, failed_files, warning_files, files_to_process,trimmed_count)

    # Detelet Empty set in output Directory
    delete_empty_directory(current_set_folder)

    return True

def timeTakenByProcess(start_time,end_time):
    # Calculate the difference in seconds
    elapsed_time = end_time - start_time
    # Convert elapsed_time to hours, minutes, and seconds
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    # Format the time taken
    time_taken = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)
    return  time_taken


if __name__ == "__main__":

    # Record the start time
    start_time = time.time()

    input_folder = "Dataset"
    output_folder = "Dataset_Converted"
    failure_folder = "Failure_Conversion"
    success_folder = "Success_Conversion"

    # set files_to_process to zero if you want to process comolete folder
    files_to_process = 5
    # set No of files in each output set.
    files_per_set = 5



    result = main(files_to_process,files_per_set,input_folder, output_folder, success_folder, failure_folder)

    # Record the end time
    end_time = time.time()

    time_taken = timeTakenByProcess(start_time, end_time)

    if result:
        print(f"Result : Successfully Completed in time {time_taken}...")
    else:
        print("Result : Failed ...")