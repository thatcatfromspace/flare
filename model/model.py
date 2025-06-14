import pickle
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import json


class LogisticRegressionModel:
    """
    Modular logistic regression model for driver acceptance prediction.
    """

    def __init__(
        self,
        model_path="driver_acceptance_model.pkl",
        features_path="model_features.json",
    ):
        self.model_path = model_path
        self.features_path = features_path
        self.model = None
        self.features = [
            "distance_to_pickup_mi",
            "dropoff_distance_mi",
            "delivery_size_lbs",
            "offered_pay_usd",
            "acceptance_rate_7d",
            "acceptance_rate_14d",
            "acceptance_rate_30d",
            "reliability_score",
            "traffic_delay_min",
            "weather_delay_factor",
            "hour_of_day",
            "day_of_week",
        ]
        self.extra_features = []
        self.X_train = self.X_test = self.y_train = self.y_test = None

    def load_data(self, csv_path):
        df = pd.read_csv(csv_path)
        df = pd.get_dummies(df, columns=["vehicle_type"], drop_first=True)
        self.extra_features = [
            col for col in df.columns if col.startswith("vehicle_type_")
        ]
        X = df[self.features + self.extra_features]
        y = df["accepted"]
        # Save feature order for scoring code
        with open(self.features_path, "w") as f:
            json.dump(self.features + self.extra_features, f)
        print("Feature order saved to", self.features_path)
        return X, y

    def preprocess_data(self, X, y, test_size=0.2, random_state=44):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

    def train(self):
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(self.X_train, self.y_train)

    def save_model(self):
        if not os.path.exists(os.path.dirname(self.model_path)):
            os.makedirs(os.path.dirname(self.model_path))
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f, protocol=5)

    def load_model(self):
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)

    def evaluate(self):
        y_pred = self.model.predict(self.X_test)
        y_proba = self.model.predict_proba(self.X_test)[:, 1]
        print(classification_report(self.y_test, y_pred))
        print("ROC AUC Score:", roc_auc_score(self.y_test, y_proba))

    def predict_proba(self, features):
        arr = np.array([features])
        return self.model.predict_proba(arr)[:, 1][0]


# --- Example usage ---
if __name__ == "__main__":
    model = LogisticRegressionModel()
    X, y = model.load_data("driver_acceptance_dataset.csv")
    model.preprocess_data(X, y)
    model.train()
    model.save_model()
    model.evaluate()

    # --- Define input vectors (in the correct order) ---
    test_cases = {
        "dream_offer": [1.2, 3.4, 10, 19.5, 92, 90, 88, 97, 2, 0.0, 9, 2, 1, 0, 0],
        "bad_offer": [8.5, 12.0, 40, 9.5, 63, 60, 58, 71, 35, 0.4, 23, 5, 0, 0, 0],
        "mid_offer": [3.5, 6.0, 20, 13.5, 75, 70, 68, 85, 8, 0.1, 14, 1, 0, 1, 0],
    }
    print("Predicted Acceptance Probabilities:")
    for label, features in test_cases.items():
        proba = model.predict_proba(features)
        print(f"{label}: {proba:.4f}")
