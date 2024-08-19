import os
from collections import Counter
from mutagen import File


def count_files_in_directory(directory_path):
    # Define paths
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_folder = os.path.join(base_path, directory_path)

    # Check if the provided path is a valid directory
    if not os.path.isdir(dataset_folder):
        print(f"{directory_path} is not a valid directory")
        return

    # List the files in the given directory (excluding subdirectories)
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    file_count = len(files)

    if file_count > 0:
        durations = []
        duration_counts = Counter()

        for f in files:
            file_path = os.path.join(directory_path, f)
            if os.path.isfile(file_path):
                try:
                    audio = File(file_path)
                    if audio is not None:
                        duration_seconds = int(audio.info.length)
                        durations.append(duration_seconds)
                        duration_counts[duration_seconds] += 1
                except Exception:
                    pass

        if durations:
            max_duration = max(durations)
            min_duration = min(durations)

            top_3_max_durations = sorted(set(durations), reverse=True)[:3]
            top_3_min_durations = sorted(set(durations))[:3]

            most_common_count = duration_counts.most_common(1)[0][1]
            most_repeated_durations = [duration for duration, count in duration_counts.items() if
                                       count == most_common_count]

            print(f"Folder: {os.path.basename(directory_path)}")
            print(f"Max: {max_duration // 60}m {max_duration % 60}s")
            print(f"Min: {min_duration // 60}m {min_duration % 60}s")
            print(f"Top 3 Max: {', '.join([f'{duration // 60}m {duration % 60}s' for duration in top_3_max_durations])}")
            print(f"Top 3 Min: {', '.join([f'{duration // 60}m {duration % 60}s' for duration in top_3_min_durations])}")
            print(f"Mode: {', '.join([f'{duration // 60}m {duration % 60}s' for duration in most_repeated_durations])}")
        else:
            print(f"No valid audio files found in {directory_path}")
    else:
        print(f"No files found in {directory_path}")

# Example usage
directory_path = "AllVoices"
count_files_in_directory(directory_path)
