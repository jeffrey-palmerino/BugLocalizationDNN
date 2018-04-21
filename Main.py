import CSVParser as CP
import MetadataFeatures as MD
import CosSim as CS
import csv

allBugReports = CP.CSVToDictionary()
count = 0
with open('features.csv', 'wb') as featureFile:
    writer = csv.writer(featureFile)
    writer.writerow(["report_id", "file", "rVSM_similarity", "collab_filter", "classname_similarity", "bug_recency", "bug_frequency"])

    for report in allBugReports:
        date = MD.convertToDateTime(report.get("report_time"))
        print "===== " + report["id"] + " ====="
        for file in report["files"]:
            try:
                srcFile = open("C:\\Users\\addis\\Desktop\\BugLocator\\EclipsePlatformUI\\" + file, 'r')
                src = srcFile.read()
                srcFile.close()

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

                writer.writerow([report["id"], file, rVSMTextSimilarity, collaborativeFilterScore, classNameSimilarity, bugFixingRecency, bugFixingFrequency])
                # print file + ": ", rVSMTextSimilarity, collaborativeFilterScore, bugFixingRecency, bugFixingFrequency
            except IOError:
                count += 1
                print "Could not read file: ", file
            except Exception:
                count += 1
                print "Something went wrong parsing this file"

featureFile.close()
print count, " files skipped"