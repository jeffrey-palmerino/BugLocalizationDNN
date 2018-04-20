import csv
from datetime import datetime
import string
import pprint

'''
A method to open a CSV file and read in data.  Converts a space delimited set of file names into a list
'''
def CSVToDictionary():
    reader = csv.DictReader(open('Eclipse_Platform_UI_Trimmed.txt', 'rb'), delimiter='\t')
    dict_list = []
    for line in reader:
        # Strip files string & split by .java (spaces in filenames). Discard empty strings & reappend .java to filenames
        line["files"] = [s.strip() + ".java" for s in line["files"].split(".java") if s]

        # Change summary & description string into list of words
        line["summary"] = cleanAndSplit(line["summary"])[2:]  # Remove first two elements of list "BUG #######"
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
Function to return a list of previously filed bug reports that share a file with the current bug report 
@params given file name in a Bug Report, the BR's date, and the dictionary of all BRs
'''
def getPreviousReportByFilename(filename, brdate, dictionary):
    return [br for br in dictionary if (filename in br["files"] and convertToDateTime(br["report_time"]) < brdate)]

'''
Helper function to convert from string to DateTime
@params the Date to be converted
'''
def convertToDateTime(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    # return datetime.strptime(date, "%m/%d/%Y %H:%M")

'''
Helper function to calculate the number of months between two date strings
@param the first date, the second date
'''
def getMonthsBetween(d1, d2):
    date1 = convertToDateTime(d1)
    date2 = convertToDateTime(d2)
    return abs((date1.year - date2.year) * 12 + date1.month - date2.month)

'''
Function to return the most recently submitted previous report that shares a filename with the given bug report
@params The filename in question, the date the current bug report was submitted, the dictionary of all bug reports
'''
def getMostRecentReport(filename, currentDate, dictionary):
    matchingReports = getPreviousReportByFilename(filename, currentDate, dictionary)
    if len(matchingReports) > 0:
        # Custom-define a lambda function to search the dictionary object for the Bug Report's time and sort by that
        return max((br for br in matchingReports), key=lambda x:convertToDateTime(x.get("report_time")))
    else:
        return None

'''
Calculate the Bug Fixing Recency as defined by Lam et al.
@params current bug report, most recent bug report
'''
def bugFixingRecency(report1, report2):
    if report1 is None or report2 is None:
        return 0
    else:
        return 1/float(getMonthsBetween(report1.get("report_time"), report2.get("report_time")) + 1)

'''
Calculate the Bug Fixing Frequency as defined by Lam et al.
@params filename fixed by BR, date of current BR, dictionary of all Bug Reports
'''
def bugFixingFrequency(filename, date, dictionary):
    return len(getPreviousReportByFilename(filename, date, dictionary))

'''
Calculate the collaborative filter score as defined by Lam et al.
@params The bug report we're calculating metadata for, the filename we're checking previous bug reports for
'''
def collaborativeFilteringScore(report, filename, dictionary):
    matchingReports = getPreviousReportByFilename(filename, convertToDateTime(report.get("report_time")), dictionary)
    # Get combined text of matching reports and do some rVSM stuff with it

'''
Function to remove all punctuation and split text strings into lists of words
'''
def cleanAndSplit(text):
    replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
    returnText = text.translate(replace_punctuation)
    returnText = [s.strip() for s in returnText.split(" ") if s];
    return returnText




allBugReports = CSVToDictionary()

# Test Bug Report Recency(You need to manually add "holaholahola.java" to at least 2 bug reports (I did the last 3))
currentReport = getMostRecentReport("holaholahola.java", convertToDateTime("2013-12-18 12:04:45"), allBugReports)
mrReport = getMostRecentReport("holaholahola.java", convertToDateTime("2013-12-17 12:04:54"), allBugReports)
# print bugFixingRecency(currentReport, mrReport)

# Test Bug Report Frequency (You need to manually add "heyheyhey.java" to at least 2 bug reports (I did the first 5))
currentReport2 = getMostRecentReport("heyheyhey.java", convertToDateTime("2013-12-10 12:12:12"), allBugReports)
# print bugFixingFrequency("heyheyhey.java", convertToDateTime(currentReport2.get("report_time")), allBugReports)

# Test looping through everything (not just manual input)
for report in allBugReports:  # loop through all reports
    # Testing File functionality
    date = convertToDateTime(report.get("report_time"))

    report["bugFixRec"] = []
    report["bugFixFreq"] = []
    for filename in report.get("files"):  # loop through each file for a report
        mostRecentReport = getMostRecentReport(filename, date, allBugReports)
        report["bugFixRec"].append(bugFixingRecency(report, mostRecentReport))
        report["bugFixFreq"].append(bugFixingFrequency(filename, date, allBugReports))

    # print report.get("bugFixRec")
    # print report.get("bugFixFreq")

    # Testing Term Frequency Functionality
    # pprint.pprint(br["summary"])
    # pprint.pprint(br["description"])
    #pprint.pprint(report["termCounts"])