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
    # raise NotImplementedError

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)

        months = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5, "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9,
                  "Nov": 10, "Dec": 11}

        evidence = []
        labels = []
        k = 0
        for row in reader:
            evidence.append([])
            for key, value in row.items():
                if key == "VisitorType":
                    evidence[k].append(int(1)) if value == "Returning_Visitor" else evidence[k].append(int(0))
                elif key == "Weekend":
                    evidence[k].append(int(1)) if value == "TRUE" else evidence[k].append(int(0))
                elif key == "Month":
                    evidence[k].append(int(months[value]))
                elif key in ["Administrative_Duration", "Informational_Duration", "ProductRelated_Duration",
                             "BounceRates", "ExitRates", "PageValues", "SpecialDay"]:
                    evidence[k].append(float(value))
                elif key in ["Administrative", "Informational", "ProductRelated", "Month", "OperatingSystems",
                             "Browser", "Region", "TrafficType", "VisitorType", "Weekend"]:
                    evidence[k].append(int(value))
                if key == "Revenue":
                    labels.append(int(1)) if value == "TRUE" else labels.append(int(0))
            k += 1
        return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # raise NotImplementedError

    knn_model = KNeighborsClassifier(n_neighbors=1)
    knn_model.fit(evidence, labels)
    return knn_model


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
    # raise NotImplementedError

    count_label_pos = 0
    count_label_neg = 0
    pos = 0
    neg = 0
    for value in labels:
        if value == 1:
            count_label_pos += 1
        elif value == 0:
            count_label_neg += 1

    for label, predict in zip(labels, predictions):
        if label == 1 and label == predict:
            pos += 1
        elif label == 0 and label == predict:
            neg += 1

    sensitivity = pos/count_label_pos
    specificity = neg/count_label_neg

    return sensitivity, specificity


if __name__ == "__main__":
    main()
