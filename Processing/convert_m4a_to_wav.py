import os
import subprocess
import shutil
from datetime import datetime

def convert_m4a_to_wav(input_folder, output_folder, failed_folder):
    try:
        # Check if output folder exists, if not, create it
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Created output directory: {output_folder}")

        # Create failedToConvert folder if it doesn't exist
        if not os.path.exists(failed_folder):
            os.makedirs(failed_folder)
            print(f"Created failed conversion directory: {failed_folder}")

        # Create current date subdirectory in failedToConvert folder
        current_date = datetime.now().strftime('%Y-%m-%d')
        failed_subfolder = os.path.join(failed_folder, current_date)
        if not os.path.exists(failed_subfolder):
            os.makedirs(failed_subfolder)
            print(f"Created subdirectory for failed conversions: {failed_subfolder}")

        # Loop through all files in the input folder
        for filename in os.listdir(input_folder):
            # Check if the file is an M4A file
            if filename.endswith(".m4a"):
                # Define full file paths
                input_file = os.path.join(input_folder, filename)
                output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + ".wav")

                # Call FFmpeg to convert the file
                result = subprocess.run(['ffmpeg', '-i', input_file, output_file], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Error converting {input_file} to {output_file}: {result.stderr}")
                    # Move the file to the failedToConvert/CurrentDate/ directory
                    shutil.move(input_file, os.path.join(failed_subfolder, filename))
                    print(f"Moved {input_file} to {failed_subfolder}")

                else:
                    print(f"Successfully converted {input_file} to {output_file}")

    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
    except OSError as os_error:
        print(f"OS error: {os_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    input_folder = "AllVoices"  # Path to the folder containing M4A files
    output_folder = "wavAudios"  # Path to the folder where WAV files will be saved
    failed_folder = "failedToConvert"  # Path to the folder where failed conversions will be saved
    convert_m4a_to_wav(input_folder, output_folder, failed_folder)
