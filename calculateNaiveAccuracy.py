import csv
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-whitegrid')

'''
Calculate Top-K Accuracy for k=1 - k=20 for our feature set
'''
def calcAccuracy():
    with open('features.csv', 'r') as f:  # CHANGE FILENAME IF YOU'RE USING IT
        next(f)  # skip column headings
        reader = csv.reader(f, delimiter=',')  # make a reader to read though the rows

        # Create the lists for each group of 1 right file and 50 wrong files
        aggregatedValues = []

        # loop though the data in the CSV and sum each feature (naive aggregation)
        for report_id, file, rVSM_similarity, collab_filter, classname_similarity, bug_recency, bug_frequency, match in reader:
            aggScore = rVSM_similarity + collab_filter + classname_similarity + bug_recency

            aggregatedValues.append([aggScore, match])
    f.close()

    topKCounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total = 0
    for group in chunker(aggregatedValues, 51): #loop through each set of 1 right & 50 wrong
        total = total + 1
        sortVals = sorted(group, key=lambda x: x[0], reverse=True)
        topKValue = [y[1] for y in sortVals].index('1')

        while topKValue < 20: # For each k value that this file is within, increment that k-value's count of correct files
            topKCounts[topKValue] = topKCounts[topKValue] + 1
            topKValue = topKValue + 1

    return topKCounts, total

'''
Function to split a list into smaller lists of a given value
'''
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

# Calculate accuracies
topKCounts, total = calcAccuracy()
accuracies = []

for position, count in enumerate(topKCounts): #loop through each k-value and calculate its accuracy
    print "Top", position+1, "Accuracy: ", count/float(total)
    accuracies.append(count/float(total) * 100)

#Plot a line graph of the accuracies
plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], accuracies, '-bo')
plt.axis([0, 20, 0, 100])
plt.xticks(np.arange(0, 21, 1.0))
plt.yticks(np.arange(0, 101, 10.0))

plt.title("Top-k Accuracy")
plt.ylabel("Accuracy")
plt.xlabel("K")
plt.show()