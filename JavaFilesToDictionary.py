import os

files = {}
start_dir = "C:\\Users\\addis\\Desktop\\BugLocator\\EclipsePlatformUI\\bundles\\"

def getAllCorpus():
    for dir,dirNames,fileNames in os.walk(start_dir):
        for filename in [f for f in fileNames if f.endswith(".java")]:
            srcName = dir + "\\" + filename
            srcFile = open(srcName, 'r')
            src = srcFile.read()
            srcFile.close()

            fileKey = srcName.split("EclipsePlatformUI\\")[1].replace("\\", "/")
            files[fileKey] = src

    return files