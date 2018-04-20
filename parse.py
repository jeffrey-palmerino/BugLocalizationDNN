import csv
import string
import pprint

'''
A method to open a CSV file and read in data.  Converts a space delimited set of file names into a list
'''
def CSVToDictionary():
    reader = csv.DictReader(open('Eclipse_Platform_UI_Trimmed.txt', 'rb'), delimiter='\t')
    dict_list = []
    for line in reader:
        #Strip string "list" of files & split by .java (there are spaces in the filenames, so we can't use that).  Discard empty strings & then reappend .java to filenames
        line["files"] = [s.strip() + ".java" for s in line["files"].split(".java") if s]

        # Change summary & description string into list of words
        line["summary"] = cleanAndSplit(line["summary"])
        line["description"] = cleanAndSplit(line["description"])
        combinedCorpus = line["summary"] + line["description"]

        # Create a dictionary with a term frequency for each term
        d = dict.fromkeys(combinedCorpus, 0)
        for i in range(len(combinedCorpus)):
            if combinedCorpus[i] in d:
                d[combinedCorpus[i]] = d[combinedCorpus[i]] + 1
            else:
                print "error for index " + i

        line["termCounts"] = d
        dict_list.append(line)
    return dict_list

'''
Function to remove all punctuation and split text strings into lists of words
'''
def cleanAndSplit(text):
    replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
    returnText = text.translate(replace_punctuation)
    returnText = [s.strip() for s in returnText.split(" ") if s];
    return returnText

#Main test
allBugReports = CSVToDictionary()

for br in allBugReports:
    #pprint.pprint(br["summary"])
    #pprint.pprint(br["description"])
    pprint.pprint(br["termCounts"])