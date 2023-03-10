import pandas as pd
import os
import glob
import json
import xlsxwriter

workbook = xlsxwriter.Workbook('../data/filtered/Dati_filtrati_all.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Atleta')
worksheet.write('B1', 'File from GPS')
worksheet.write('C1', 'File Time')
worksheet.write('D1', 'Day')
worksheet.write('E1', 'Time')
row = 1

df = pd.DataFrame(columns=["Atleta", "File_gps", "File_time", "Day", "DNF", "StartTime", "Time"])

for day in ["G1", "P1", "P2"]:
    data_folder = f'../data/{day}'
    timing_json = f'../data/{day}/timing-data-{day}.json'
    files = glob.glob(os.path.join(data_folder, '*-resampled.csv'))
    files.sort()

    with open(timing_json) as json_file:
        timing = json.load(json_file)['records']
        # ony look at timing data from given profile
        timing = [run
                    for run in timing
                        if 'profile' in run and run['profile']['id']
                == 'cbb60118-cd9e-4dd7-9418-066832b9e9ed']
        for fileName in files:
            data = pd.read_csv(fileName)
            # check if data covers one run

            runs_of_filename = []
            for run in timing:
                if 'totalDuration' in run:
                    runData = data[(data['Timestamp'] >= run['startedAt']) & (data['Timestamp'] <= run['startedAt'] + run['totalDuration'])]
                    if not runData.empty:
                        worksheet.write(row, 0, run['label'])
                        worksheet.write(row, 1, fileName)
                        worksheet.write(row, 2, run["id"])
                        worksheet.write(row, 3, day)
                        worksheet.write(row, 4, run["totalDuration"])
                        label, index_label = run['label'].lower(), 2
                        while label in df["Atleta"].to_numpy():
                            label = f"{run['label'].lower()}_{index_label}"
                            index_label += 1
                        
                        dnf = "dnf" in label.lower()
                        df.loc[len(df)] = [label, fileName, run["id"], day, dnf, run["startedAt"], run["totalDuration"]]
                        row +=1
                        
                        runs_of_filename.append(run["id"])
            print(fileName, "has", runs_of_filename)
workbook.close()
df.to_csv("../data/filtered/Dati_filtrati_all.csv", index = False)