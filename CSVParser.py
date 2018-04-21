import csv
import string

'''
A method to open a CSV file and read in data.  Converts a space delimited set of file names into a list
'''
def CSVToDictionary():
    reader = csv.DictReader(open('Eclipse_Platform_UI.txt', 'rb'), delimiter='\t')
    dict_list = []
    for line in reader:
        # Strip files string & split by .java (spaces in filenames). Discard empty strings & reappend .java to filenames
        line["files"] = [s.strip() + ".java" for s in line["files"].split(".java") if s]

        line["rawCorpus"] = line["summary"][10:] + line["description"]

        # Change summary & description string into list of words
        line["summary"], line["description"], combinedCorpus = getCombinedCorpus(line)

        '''
        # Create a dictionary with a term frequency for each term
        d = dict.fromkeys(combinedCorpus, 0)
        for i in range(len(combinedCorpus)):
            if combinedCorpus[i] in d:
                d[combinedCorpus[i]] = d[combinedCorpus[i]] + 1
            else:
                print "error for index " + i

        line["termCounts"] = d
        '''
        dict_list.append(line)
    return dict_list


'''
Function to create a combined corpus out of a bug report
@param a bug report
'''
def getCombinedCorpus(report):
    report["summary"] = cleanAndSplit(report["summary"])[2:]  # Remove first two elements of list "BUG #######"
    report["description"] = cleanAndSplit(report["description"])
    combinedCorpus = report["summary"] + report["description"]
    return report["summary"], report["description"], combinedCorpus

'''
Function to remove all punctuation and split text strings into lists of words
'''
def cleanAndSplit(text):
    replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
    returnText = text.translate(replace_punctuation)
    returnText = [s.strip() for s in returnText.split(" ") if s];
    return returnText