import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    A = {
        'Jan':1,
        'Feb':2,
        'Mar':3,
        'Apr':4,
        'May':5,
        'June':6,
        'Jul':7,
        'Aug':8,
        'Sep':9,
        'Oct':10,
        'Nov':11,
        'Dec':12
    }
    E = []
    P = []
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        data = []
        for line in reader:
            evidence = []
            evidence = [int(line[0]),float(line[1]),int(line[2]),float(line[3]),int(line[4])]
            for x in range(5,10):
                evidence.append(float(line[x]))
            evidence.append(int(A[line[10]] - 1))
            for x in range(11,15):
                evidence.append(int(line[x]))            
            if line[15] == 'Returning_Visitor':
                evidence.append(int(1))
            else:
                evidence.append(int(0))
            if line[16] == 'True':
                evidence.append(int(1))
            else:
                evidence.append(int(0))                
            E.append(evidence)
            P.append(int(1) if line[17] == 'TRUE' else int(0))
    return (E,P)
    raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # model = KNeighborsClassifier(n_neighbors = 1)
    # model.fit(evidence,labels)
    # return model
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    n = len(labels)
    sen = 0
    nsen = 0
    spe = 0
    nspe = 0
    # print(labels)
    for i in range(n):
        if(labels[i] == 1):
            nsen += 1 
            if(labels[i] == predictions[i]):
                sen += 1
        else:
            nspe += 1 
            if(labels[i] == predictions[i]):
                spe += 1
    return ((sen / nsen),(spe / nspe))
    raise NotImplementedError


if __name__ == "__main__":
    main()
