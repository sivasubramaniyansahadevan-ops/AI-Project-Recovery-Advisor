import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

df = pd.read_csv("project_rescue_ai_500_rows.csv")

features = [
    "cost_variance_percent",
    "schedule_variance_percent",
    "schedule_variance_days",
    "spi",
    "cpi",
    "completed_tasks_percent",
    "open_risks_count",
    "open_issues_count",
    "scope_changes_count",
    "resource_utilization_percent",
    "stakeholder_sentiment_score",
    "risk_score"
]

X = df[features]
y = df["status"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))

joblib.dump(model, "project_rescue_model.pkl")
print("Model saved as project_rescue_model.pkl")
