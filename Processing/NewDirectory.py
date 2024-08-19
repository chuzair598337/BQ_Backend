import os
from collections import defaultdict
from prettytable import PrettyTable
from mutagen import File

def count_files_in_directory(directory_path):
    # Check if the provided path is a valid directory
    if not os.path.isdir(directory_path):
        print(f"{directory_path} is not a valid directory")
        return

    # Create the Log folder if it doesn't exist
    log_dir = os.path.join(directory_path, "Log")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create the log file path
    log_file_path = os.path.join(log_dir, "directory_log.txt")

    # Create a PrettyTable object
    table = PrettyTable()
    table.field_names = ["Folder Name", "File Count", "File Types", "Detailed Count", "File Durations", "Count >1s", "Files >1s"]

    # Walk through the directory
    for root, dirs, files in os.walk(directory_path):
        # Count files in the current directory (excluding subdirectories)
        file_count = len(files)
        if file_count > 0:
            current_dir = os.path.relpath(root, directory_path)

            # Create a defaultdict to store file type counts
            file_type_counts = defaultdict(int)
            file_durations = []
            files_gt_1s = []
            count_gt_1s = 0

            for f in files:
                file_path = os.path.join(root, f)
                if os.path.isfile(file_path):
                    ext = os.path.splitext(f)[1][1:]  # Remove the leading dot
                    file_type_counts[ext] += 1

                    # Get file duration for audio files
                    try:
                        audio = File(file_path)
                        if audio is not None:
                            duration_seconds = int(audio.info.length)
                            minutes, seconds = divmod(duration_seconds, 60)
                            duration_str = f"{minutes}m {seconds}s"
                            file_durations.append(f"{f}: {duration_str}")
                            if duration_seconds > 1:
                                count_gt_1s += 1
                                files_gt_1s.append(f)
                    except Exception as e:
                        pass

            file_types_str = ", ".join(sorted(file_type_counts.keys()))
            detailed_count_str = ", ".join([f"{ext}:{count}" for ext, count in sorted(file_type_counts.items())])
            file_durations_str = ", ".join(file_durations)
            files_gt_1s_str = ", ".join(files_gt_1s)

            table.add_row([current_dir, file_count, file_types_str, detailed_count_str, file_durations_str, count_gt_1s, files_gt_1s_str])

    # Write the table to the log file
    with open(log_file_path, "w") as log_file:
        log_file.write(str(table))

    # Print the table
    print(table)

# Example usage
directory_path = r"C:\Users\Saif_Ali\Downloads\Data"
count_files_in_directory(directory_path)
