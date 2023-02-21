import pandas as pd
import os
import glob
import json
import xlsxwriter

data_folder = '../data/G1'
timing_json = '../data/G1/timing-data-G1.json'
row = 1
workbook = xlsxwriter.Workbook('../data/filtered/Dati_filtrati.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Atleta')
worksheet.write('B1', 'File')
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
        print(' ')
        print("File Name:")
        print(fileName)
        data = pd.read_csv(fileName)
        # check if data covers one run
        for run in timing:
            if 'totalDuration' in run:
                runData = data[(data['Timestamp'] >= run['startedAt']) & (data['Timestamp'] <= run['startedAt'] + run['totalDuration'])]
                if not runData.empty:
                    worksheet.write(row, 0, run['label'])
                    worksheet.write(row, 1, fileName)
                    print('Athlete: ' + run['label'])
                    print('Data found!')
                    print(row)
                    row +=1
                    print('*************************************************')
                    # You can use runData now for whatever processing you like to do
workbook.close()
