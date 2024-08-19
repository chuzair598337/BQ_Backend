import pandas as pd
import os

file_path = 'old_selected_data.sql'


def createExcelFile(tableName):
    file_name = f"{tableName}.xlsx"
    return os.path.join(output_folder, file_name)

if not os.path.exists(file_path):
    print(f"File '{file_path}' does not exist.")
else:

    # Create the output folder if it does not exist
    output_folder = 'sheets'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    line_count = 0
    quran_urdu_df = pd.DataFrame(columns=["surahID", "verseID", "verseUrduText"])
    reciter_df = pd.DataFrame(columns=["surahID", "verseID", "verseFileName"])
    Quran_df = pd.DataFrame(columns=["surahID", "verseID", "verseArabicText"])

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            valuesSplit = line.strip().split("VALUES")
            spaceSplit_1 = valuesSplit[0].strip().split()
            tableName = spaceSplit_1[2].strip('"')

            rawData = valuesSplit[1][1:]
            removeSemicolon = rawData[1:]
            removeParenthesis = removeSemicolon[1:-2]
            splitRawData = removeParenthesis.strip().split(',')

            if tableName == "quran_urdu":
                SuraID = splitRawData[1]
                VerseID = splitRawData[2]
                AyahText = splitRawData[3].strip("'") # remove single Quote ( ' ) from both ends.
                # Append the data to the DataFrame
                quran_urdu_df = pd.concat([quran_urdu_df, pd.DataFrame([{
                    "surahID": SuraID,
                    "verseID": VerseID,
                    "verseUrduText": AyahText
                }])], ignore_index=True)

            elif tableName == "reciter":
                SuraID = splitRawData[3]
                VerseID = splitRawData[2]
                Audio_URL = splitRawData[1].strip("'") # remove single Quote ( ' ) from both ends.
                # Append the data to the DataFrame
                reciter_df = pd.concat([reciter_df, pd.DataFrame([{
                    "surahID": SuraID,
                    "verseID": VerseID,
                    "verseFileName": Audio_URL
                }])], ignore_index=True)

            elif tableName == "Quran":
                SuraID = splitRawData[2]
                VerseID = splitRawData[3]
                AyahText = splitRawData[4].strip("'") # remove single Quote ( ' ) from both ends.
                # Append the data to the DataFrame
                Quran_df = pd.concat([Quran_df, pd.DataFrame([{
                    "surahID": SuraID,
                    "verseID": VerseID,
                    "verseArabicText": AyahText
                }])], ignore_index=True)

            line_count += 1

    print(f'Total number of SQL insert statements: {line_count}')

    # Save DataFrames to Excel files
    quran_urdu_file = createExcelFile("quran_urdu")
    Quran_file = createExcelFile("Quran")
    reciter_file = createExcelFile("reciter")

    quran_urdu_df.to_excel(quran_urdu_file, index=False)
    Quran_df.to_excel(Quran_file, index=False)
    reciter_df.to_excel(reciter_file, index=False)

    print("Sheets Created Successfully...")

    ####################################################

    merged_df = pd.merge(quran_urdu_df, Quran_df)
    merged_df = pd.merge(merged_df, reciter_df)

    print(merged_df.columns)

    # Create the new DataFrame with auto-incrementing ID
    QuranEPak_df = pd.DataFrame({
        'quranEPakID': range(1, len(merged_df) + 1),  # Auto-incremented IDs
        'surahID': merged_df['surahID'],
        'verseID': merged_df['verseID'],
        'verseFileName': merged_df['verseFileName'],
        'verseArabicText': merged_df['verseArabicText'],
        'verseUrduText': merged_df['verseUrduText'],
    })

    # Save the new DataFrame to an Excel file
    output_file = 'QuranEPak.xlsx'
    QuranEPak_df.to_excel(output_file, index=False)

    print(f"Merged DataFrame saved successfully as {output_file}")