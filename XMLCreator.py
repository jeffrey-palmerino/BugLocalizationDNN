import csv
import datetime
import xml.etree.ElementTree as ET
import pprint

'''
A method to open a CSV file and read in data.  Converts a space delimited set of file names into a list
'''
def CSVToDictionary():
    reader = csv.DictReader(open('Eclipse_Platform_UI.txt', 'rb'), delimiter='\t')
    dict_list = []
    for line in reader:
        # Strip files string & split by .java (spaces in filenames). Discard empty strings & reappend .java to filenames
        line["files"] = [s.strip() + ".java" for s in line["files"].split(".java") if s]
        line["commit_timestamp"] = datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S')

        dict_list.append(line)
    return dict_list

bugReports = CSVToDictionary()

pprint.pprint(bugReports)

EclipseUIBugRepository = open('EclipseUIBugRepository.xml', 'w')
root = ET.Element('bugrepository')
root.set('name', "EclipseUI")

for b in bugReports:
    bug = ET.SubElement(root, 'bug')
    bug.set('id', b["bug_id"])
    bug.set('opendate', b["report_time"])
    bug.set('fixdate', b["commit_timestamp"])

    buginformation = ET.SubElement(bug, 'buginformation')

    summary = ET.SubElement(buginformation, 'summary')
    summary.text = b["summary"]

    description = ET.SubElement(buginformation, 'description')
    description.text = b["description"]

    fixedFiles = ET.SubElement(bug, 'fixedFiles')
    for f in b["files"]:  # Maybe convert these to org.eclipse.ui rather than org/eclipse/ui ??
        file = ET.SubElement(fixedFiles, 'file')
        file.text = f

tree = ET.ElementTree(root)
tree.write(EclipseUIBugRepository)
EclipseUIBugRepository.close()