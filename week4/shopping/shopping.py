import csv
import sys
import calendar

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
    data = []
    labels = []
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        convert = converters()
        for row in reader:
            converted = [convert[col](row[col]) if col in convert else row[col] for col in reader.fieldnames]
            print(converted)
            data.append(converted[:-1])
            labels.append(converted[-1])
    return data, labels


def train_model(evidence, labels):
    print("trainmodellabels", labels)
    k = KNeighborsClassifier(n_neighbors=1)
    k.fit(evidence, labels)
    return k

def evaluate(labels, predictions):
    true_positive = 0
    true_negative = 0
    total_positive = 0
    total_negative = 0
    for l, p in zip(labels, predictions):
        if l == 1:
            total_positive += 1
            if p == 1:
                true_positive += 1
        else:
            total_negative += 1
            if p == 0:
                true_negative += 1
    sensitivity = true_positive / total_positive if total_positive else 0
    specificity = true_negative / total_negative if total_negative else 0
    return sensitivity, specificity


def converters():
    converter = {
        "Administrative": int,
        "Informational": int,
        "ProductRelated": int,
        "Month": convert_month,
        "OperatingSystems": int,
        "Browser": int,
        "Region": int,
        "TrafficType": convert_bool,
        "VisitorType": convert_bool, 
        "Weekend": convert_bool,
        "Administrative_Duration": float,
        "Informational_Duration": float,
        "ProductRelated_Duration": float,
        "BounceRates": float,
        "ExitRates": float,
        "PageValues": float,
        "SpecialDay": float,
        "Revenue": convert_bool

    }
    return converter


def convert_month(month):
    if month in ("June", "june"):
        return 5
    month_lookup = {month: i - 1 for i, month in enumerate(calendar.month_abbr) if month}
    return month_lookup[month]

def convert_bool(v):
    v = v.strip().lower()
    return 1 if v in ("true", "returning_visitor") else 0

if __name__ == "__main__":
    main()
