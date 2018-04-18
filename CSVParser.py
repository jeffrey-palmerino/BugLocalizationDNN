import csv
import pprint

'''
A method to open a CSV file and read in data
'''
def CSV_To_Dictionary():
    reader = csv.DictReader(open('Eclipse_Platform_UI_Trimmed.csv', 'rb'), delimiter='\t')
    dict_list = []
    for line in reader:
        line["files"] = [s.strip() + ".java" for s in line["files"].split(".java") if s]
        dict_list.append(line)
    return dict_list

device_values = CSV_To_Dictionary()
pprint.pprint(device_values)
