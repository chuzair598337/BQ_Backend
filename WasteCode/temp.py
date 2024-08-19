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

    print(report)
    return report


# Example data
suras_List = [
    ("Sura1", 10, {"wav": 5, "mp3": 5}),
    ("Sura2", 8, {"wav": 4, "mp3": 4})
]

commands_List = [
    ("Command1", 12, {"wav": 6, "mp3": 6}),
    ("Command2", 15, {"wav": 8, "mp3": 7})
]

# Generate and print the report
report = generateReport(suras_List, commands_List)

# Save the report to a log file
with open("report.log", "w") as log_file:
    log_file.write(report)
