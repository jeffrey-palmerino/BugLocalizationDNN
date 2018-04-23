import CSVParser as CP
import MetadataFeatures as MD
import CosSim as CS
import JavaFilesToDictionary as JF
import csv
import random

allBugReports = CP.CSVToDictionary()
javaFiles = JF.getAllCorpus()
print len(javaFiles)
count = 0

def getTop50WrongFiles(rightFiles, brCorpus):
    randomlySampled = random.sample(list(javaFiles), 100)  # Randomly sample 100 out of the 3,981 files so we can get this done before I graduate

    allFiles = []
    for filename in [f for f in randomlySampled if f not in rightFiles]:
        try:
            rawClassNames = javaFiles[filename].split(" class ")[1:]

            classNames = []
            for block in rawClassNames:
                classNames.append(block.split(' ')[0])
            classCorpus = ' '.join(classNames)

            one = CS.cosine_sim(brCorpus, javaFiles[filename])
            two = CS.cosine_sim(brCorpus, classCorpus)

            fileInfo = [filename, one, two]
            allFiles.append(fileInfo)
        except Exception:
            print "Error in wrong file parsing"
            del javaFiles[filename]

    topfifty = sorted(allFiles, key=lambda x: x[1], reverse=True)[:50]
    return topfifty


with open('features.csv', 'wb') as featureFile:
    writer = csv.writer(featureFile)
    writer.writerow(["report_id", "file", "rVSM_similarity", "collab_filter", "classname_similarity", "bug_recency", "bug_frequency", "match"])

    for report in allBugReports:
            date = MD.convertToDateTime(report.get("report_time"))
            rawCorpus = report["rawCorpus"]
            files = report["files"]

            print "===== " + report["id"] + " ====="
            try:
                for file in report["files"]:
                    src = javaFiles[file]

                    # rVSM Text Similarity
                    rVSMTextSimilarity = CS.cosine_sim(report["rawCorpus"], src)

                    # Collaborative Filter Score
                    prevReports = MD.getPreviousReportByFilename(file, date, allBugReports)
                    relatedCorpus = []
                    for report in prevReports:
                        relatedCorpus.append(report["rawCorpus"])
                    relatedString = ' '.join(relatedCorpus)
                    collaborativeFilterScore = CS.cosine_sim(report["rawCorpus"], relatedString)

                    # Class Name Similarity
                    rawClassNames = src.split(" class ")[1:]

                    classNames = []
                    for block in rawClassNames:
                        classNames.append(block.split(' ')[0])
                    classCorpus = ' '.join(classNames)
                    classNameSimilarity = CS.cosine_sim(report["rawCorpus"], classCorpus)

                    # Bug Fixing Recency
                    mrReport = MD.getMostRecentReport(file, MD.convertToDateTime(report["report_time"]), allBugReports)
                    bugFixingRecency = MD.bugFixingRecency(report, mrReport)

                    # Bug Fixing Frequency
                    bugFixingFrequency = MD.bugFixingFrequency(file, date, allBugReports)

                    writer.writerow([report["id"], file, rVSMTextSimilarity, collaborativeFilterScore, classNameSimilarity, bugFixingRecency, bugFixingFrequency, 1])

                    for wr in getTop50WrongFiles(report["files"], report["rawCorpus"]):
                        writer.writerow([report["id"], wr[0], wr[1], collaborativeFilterScore, wr[2], bugFixingRecency, bugFixingFrequency, 0])
                    print "~~~~~~~~~~"
            except IOError:
                count += 1
                print "Could not read file"
            except Exception:
                count += 1
                print "Something went wrong parsing this file"

featureFile.close()
print count, " files skipped"