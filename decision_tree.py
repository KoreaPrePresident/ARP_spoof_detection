import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix



FILE = "processed_dataset_no_mac.csv"

df = pd.read_csv(FILE)



features = [
    "ttl",
    "proto",
    "Len",
    "interval",
    "pps",
    "jitter"
]


X = df[features]
y = df["Label"]




X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)



model = DecisionTreeClassifier(
    criterion="gini",
    max_depth=14,
    random_state=42
)


model.fit(
    X_train,
    y_train
)



pred = model.predict(X_test)


accuracy = accuracy_score(
    y_test,
    pred
)


print("Accuracy :", accuracy)

print("\nClassification Report")
print(
    classification_report(
        y_test,
        pred
    )
)


print("\nConfusion Matrix")
print(
    confusion_matrix(
        y_test,
        pred
    )
)




print("\nFeature Importance")

for name, importance in zip(
    features,
    model.feature_importances_
):
    print(
        f"{name}: {importance:.5f}"
    )


with open(
    "arp_detector_no_mac.pkl",
    "wb"
) as f:

    pickle.dump(
        model,
        f
    )


print("\nmodel saved")