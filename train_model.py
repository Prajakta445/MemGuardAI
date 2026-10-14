
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

# Load collected memory data
df = pd.read_csv("memory_data.csv")

# Remove invalid records
df = df.dropna(subset=["memory_mb"])

# Train on memory usage values
X = df[["memory_mb"]]

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(X)

# Detect unusual memory values
df["prediction"] = model.predict(X)

df["status"] = df["prediction"].map({
    1: "Normal",
    -1: "Suspicious"
})

# Save results and trained model
df.to_csv("memory_analysis.csv", index=False)
joblib.dump(model, "memguard_model.pkl")

print("Model training completed.")
print("Total records:", len(df))
print("\nDetection summary:")
print(df["status"].value_counts())
print("\nFiles saved:")
print("- memory_analysis.csv")
print("- memguard_model.pkl")
