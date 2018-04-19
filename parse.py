# -*- coding: utf-8 -*-
import csv
import string

count = 0
with open('some.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile,delimiter=',')
    for row in csvReader:
    	word = row[0]
        splitted = word.split(" ")
        splitted = splitted.translate(None, string.punctuation)
        d = dict.fromkeys(splitted, 0)
        for i in range(len(splitted)):
			if splitted[i] in d:
				d[splitted[i]] = d[splitted[i]] + 1
			else:
				print("error")				
