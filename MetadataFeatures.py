from datetime import datetime

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