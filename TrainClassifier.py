import pickle, csv, math, random, nltk
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
from nltk.classify import MaxentClassifier

def CSV_To_Dictionary():
    with open('features.csv', 'r') as f:
        next(f)  # skip column headings
        reader = csv.reader(f, delimiter=',')  # make a reader to read though the rows

        # Create the lists for each type of classification
        right = []
        wrong = []

        # loop though the data in the CSV and add each question to it's corresponding list
        for report_id, file, rVSM_similarity, collab_filter, classname_similarity, bug_recency, bug_frequency, match in reader:
            if match == "1":
                print("right")
                right.append([rVSM_similarity, collab_filter, classname_similarity, bug_recency, bug_frequency]);
            else:
                wrong.append([rVSM_similarity, collab_filter, classname_similarity, bug_recency, bug_frequency]);
    f.close()

    # Actually split the data from 1 list into the train/dev/test lists
    rightTrain, rightTest = split_data(right)
    wrongTrain, wrongTest = split_data(wrong)

    # Format the data as a dictionary - not the most efficient way of doing it, but it quickly allowed me to reformat this as 3 dictionaries
    trainingData = {
        'right': rightTrain,
        'wrong': wrongTrain,
    }

    # These are only tagged to evaluate accuracy and to keep the data in a format acceptable by the classifier.
    # The tags are at NEVER shown to the classifiers and are only used to evaluate accuracy at the end
    testData = {
        'right': rightTest,
        'wrong': wrongTest,
    }

    return trainingData, testData


'''
A method to randomly split a given list of data into 3 lists - a training list, a dev list, and a testing list
'''
def split_data(questionList):
    # Perform the necessary mathematical calculations to perform a 70%/15%/15% split
    length = len(questionList)
    endTrain = int(math.floor(0.7 * length))

    random.shuffle(questionList)  # shuffle the data to ensure a random training set

    # Split and return the data into two lists
    return questionList[:endTrain], questionList[endTrain:]


'''
A method to plot a confusion Matrix for a classifier
'''
def PlotConfusionMatrix( \
        confusionMatrix,
        classifier,
        title='Confusion matrix',
        cmap=plt.cm.Blues
):
    plt.imshow( \
        confusionMatrix,
        interpolation='nearest',
        cmap=cmap
    )

    # Feature creation/addition for the Confusion Matrix
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classifier.labels()))
    plt.xticks(tick_marks, classifier.labels(), rotation=45)
    plt.yticks(tick_marks, classifier.labels())
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


'''
A method to evaluate classifier's accuracy on a testSet and create a confusion matrix
'''
def EvaluateClassifier(classifier, testSet, testLabeledData, possibleClassifications):
    print("Classifier's accuracy values:")

    onTestSetAccuracy = nltk.classify.accuracy(classifier, testSet)

    print("\tOn test set = {}".format(onTestSetAccuracy))

    # List to store the cases where the algorithm made a mistake
    errorCases = []

    rightCount = 0
    wrongCount = 0
    rightRight = 0
    wrongRight = 0

    # plotting Confusion Matrix
    y_test, y_pred = [], []
    for (tag, features) in testLabeledData.items():
        # Find errors
        for feature in features:
            guess = classifier.classify((dict([(i, True) for i in feature])))

            if tag == "0":
                wrongCount = wrongCount + 1
                if guess == "0":
                    wrongRight = wrongRight + 1
            elif tag == "1":
                rightCount = rightCount + 1
                if guess == "1":
                    rightRight = rightRight + 1

            if guess is None or tag is None:  continue
            y_pred.append(possibleClassifications.index(guess))
            y_test.append(possibleClassifications.index(tag))

            if guess != tag:
                caseDescription = "feature: {0} prediction:{1}, real: {2}".format(feature, guess, tag)
                errorCases.append(caseDescription)

    # Create the confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    np.set_printoptions(precision=2)
    print('\n\nConfusion matrix, without normalization for the Classifier\n')
    print(cm)
    plt.figure()
    PlotConfusionMatrix(cm, classifier)

    return errorCases


train, test = CSV_To_Dictionary()
labeledTrain = []
labeledTest = []
possibleClassifications = ['right', 'wrong']

print("----------EXTRACTING FEATURES----------")
print("TRAINING SET")
for classification, features in train.items():
    print("\t" + classification)
    for position, feature in enumerate(features):
        print("\t\t" + str(position+1) + " of " + str(len(features)))
        labeledTrain.append((dict([(i, True) for i in feature]), classification))

print("TEST SET (for accuracy purposes)")
for classification, features in test.items():
    print("\t" + classification)
    for position, feature in enumerate(features):
        print("\t\t" + str(position+1) + " of " + str(len(features)))
        labeledTest.append((dict([(i, True) for i in feature]), classification))

print("\n\n----------TRAINING CLASSIFIERS----------")
print("\t-----Maxent-----")
maxent = MaxentClassifier.train(labeledTrain)
print("\t-----Naive Bayes-----")
nb = nltk.NaiveBayesClassifier.train(labeledTrain)

maxentErrors = EvaluateClassifier(maxent, labeledTest, test, possibleClassifications)
nbError = EvaluateClassifier(nb, labeledTest, test, possibleClassifications)

outfile = open('maxent.pickle', 'wb')
pickle.dump(maxent, outfile)
outfile.close()

outfile = open('nb.pickle', 'wb')
pickle.dump(nb, outfile)
outfile.close()