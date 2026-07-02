
# STEP 4: Train ML Model + Measure Fairness
# Dataset: Adult Income (same one used in R)


import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("Loading dataset")

# Load the same clean dataset you created in R
df = pd.read_csv("data/adult_clean.csv")

# Quick check
print(f"\nDataset shape: {df.shape}")
print(df.head())

# ---- Clean income column ----
df['income'] = df['income'].str.strip()

# ---- Drop rows with missing values ----
df = df.dropna()
print(f"\nRows after dropping missing values: {len(df)}")

# ---- Keep a copy of original sex/race for fairness analysis later ----
df['sex_original'] = df['sex']
df['race_original'] = df['race']

# ---- Encode categorical columns for the model ----
categorical_cols = ['workclass', 'education', 'marital_status', 'occupation',
                     'relationship', 'race', 'sex', 'native_country', 'income']

encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le  # save encoder in case we need to decode later

# ---- Define features (X) and target (y) ----
X = df.drop(columns=['income', 'sex_original', 'race_original'])
y = df['income']  # 0 = <=50K, 1 = >50K (LabelEncoder assigns alphabetically)

print(f"\nIncome encoding check: {dict(zip(encoders['income'].classes_, encoders['income'].transform(encoders['income'].classes_)))}")

# ---- Train-test split ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTraining set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# ---- Train Random Forest model ----
print("\nTraining Random Forest model")
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model.fit(X_train, y_train)

# ---- Evaluate ----
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n Model Performance ")
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['<=50K', '>50K']))

# ---- Save test data + predictions for fairness analysis (next script) ----
results_df = X_test.copy()
results_df['y_true'] = y_test.values
results_df['y_pred'] = y_pred
results_df.to_csv("data/model_predictions.csv", index=False)
print("\nPredictions saved to data/model_predictions.csv")