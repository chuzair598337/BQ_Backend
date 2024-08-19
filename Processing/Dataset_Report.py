import os
import datetime
from tabulate import tabulate

def generateReport(suras_List, commands_List):
    # Generate report
    report = "Report:\n\n"
    report += "Data in Dataset/Suras\n"
    suras_headers = ["Folder Name", "No of Audio Files", "Different Count of Files"]
    suras_table = [[detail[0], detail[1], list(detail[2].items())] for detail in suras_List]
    suras_report = tabulate(suras_table, headers=suras_headers, tablefmt="grid",
                            colalign=("center", "center", "center"))

    report += suras_report
    report += "\n\nData in Dataset/Commands\n"
    commands_headers = ["Folder Name", "No of Audio Files", "Different Count of Files"]
    commands_table = [[detail[0], detail[1], list(detail[2].items())] for detail in commands_List]
    commands_report = tabulate(commands_table, headers=commands_headers, tablefmt="grid",
                               colalign=("center", "center", "center"))

    report += "\n" + commands_report

    return report

def saveReport(report,log_folder,):
    # Log the report with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_folder, f"log_{timestamp}.txt")

    with open(log_file, "w") as file:
        file.write(report)

    print(f"MSG :File ({os.path.relpath(log_file)}) Saved Successfully in {os.path.relpath(log_folder)}")

# Function to collect details
def collect_details(root, subdirs, detail_list):
    for subdir in subdirs:
        subdir_path = os.path.join(root, subdir)
        if os.path.isdir(subdir_path):
            file_types_count = {}
            total_files = 0
            for _, _, filenames in os.walk(subdir_path):
                for f in filenames:
                    file_type = f.split('.')[-1]
                    if file_type in file_types_count:
                        file_types_count[file_type] += 1
                    else:
                        file_types_count[file_type] = 1
                    total_files += 1
            detail_list.append([subdir, total_files, file_types_count])

def main(dataset_folder,log_folder):
    # Define paths
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_folder = os.path.join(base_path, "Dataset")
    log_folder = os.path.join(base_path, "logs")

    if not os.path.exists(dataset_folder):
        print(f"Error[0] : {os.path.relpath(dataset_folder)} directory not found...")
        return False

    # Ensure the log folder exists
    if not os.path.exists(log_folder):
        print(f"MSG : {log_folder} directory Created...")
        os.makedirs(log_folder)

    # Initialize detail lists
    Dataset_Suras_Detail_List = []
    Dataset_Commands_Detail_List = []

    # Collect details for Suras
    suras_path = os.path.join(dataset_folder, "Suras")
    if os.path.exists(suras_path):
        suras_subdirs = os.listdir(suras_path)
        collect_details(suras_path, suras_subdirs, Dataset_Suras_Detail_List)

    # Collect details for Commands
    commands_path = os.path.join(dataset_folder, "Commands")
    if os.path.exists(commands_path):
        commands_subdirs = os.listdir(commands_path)
        collect_details(commands_path, commands_subdirs, Dataset_Commands_Detail_List)

    report = generateReport(Dataset_Suras_Detail_List,Dataset_Commands_Detail_List)

    # Print Report
    print(report)

    # Save report to Logs
    saveReport(report,log_folder)

if __name__ == "__main__":

    dataset_folder = "Dataset"
    log_folder = "logs"

    main(dataset_folder,log_folder)
