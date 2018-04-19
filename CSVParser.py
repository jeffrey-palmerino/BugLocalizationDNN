import csv
from datetime import datetime

'''
A method to open a CSV file and read in data.  Converts a space delimited set of file names into a list
'''
def CSVToDictionary():
    reader = csv.DictReader(open('Eclipse_Platform_UI_Trimmed.csv', 'rb'), delimiter='\t')
    dict_list = []
    for line in reader:
        #Strip string "list" of files & split by .java (there are spaces in the filenames, so we can't use that).  Discard empty strings & then reappend .java to filenames
        line["files"] = [s.strip() + ".java" for s in line["files"].split(".java") if s]
        dict_list.append(line)
    return dict_list

'''
Function to return a list of previously filed bug reports that share a file with the current bug report 
@params given file name in a Bug Report, the BR's date, and the dictionary of all BRs
'''
def getPreviousReportByFilename(filename, date, dictionary):
    return [br for br in dictionary if (filename in br["files"] and convertToDateTime(br["report_time"]) < date)]

'''
Helper function to convert from string to DateTime
@params the Date to be converted
'''
def convertToDateTime(date):
    #return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return datetime.strptime(date, "%m/%d/%Y %H:%M")

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

    #Custom-define a lambda function to search the dictionary object for the Bug Report's time and sort by that
    return max((br for br in matchingReports), key=lambda x:convertToDateTime(x.get("report_time")))

'''
Calculate the Bug Fixing Recency as defined by Lam et al.
@params current bug report, most recent bug report
'''
def bugFixingRecency(report1, report2):
    return 1/float(getMonthsBetween(report1.get("report_time"), report2.get("report_time")) + 1)

'''
Calculate the Bug Fixing Frequency as defined by Lam et al.
@params filename fixed by BR, date of current BR, dictionary of all Bug Reports
'''
def bugFixingFrequency(filename, date, dictionary):
    return len(getPreviousReportByFilename(filename, date, dictionary))

#MAIN FUNCTIONALITY
device_values = CSVToDictionary()

#Test Bug Report Recency(Note: You need to manually add "holaholahola.java" to at least 2 bug reports (I did the last 3))
currentReport = getMostRecentReport("holaholahola.java", convertToDateTime("12/18/2013 12:04"), device_values)
mrReport = getMostRecentReport("holaholahola.java", convertToDateTime("12/17/2013 12:04"), device_values)
print bugFixingRecency(currentReport, mrReport)

#Test Bug Report Frequency (Note: You need to manually add "heyheyhey.java" to at least 2 bug reports (I did the first 5))
currentReport2 = getMostRecentReport("heyheyhey.java", convertToDateTime("12/10/2013 12:12"), device_values)
print bugFixingFrequency("heyheyhey.java", convertToDateTime(currentReport2.get("report_time")), device_values)
