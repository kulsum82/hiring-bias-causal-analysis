
Bias Mitigation Using Fairlearn


import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from fairlearn.reductions import ExponentiatedGradient, DemographicParity
from fairlearn.metrics import MetricFrame, demographic_parity_difference, equalized_odds_difference

print("Loading and preparing data")

#  Load and clean data
df = pd.read_csv("data/adult_clean.csv")
df['income'] = df['income'].str.strip()
df = df.dropna()

categorical_cols = ['workclass', 'education', 'marital_status', 'occupation',
                     'relationship', 'race', 'sex', 'native_country', 'income']

encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df.drop(columns=['income'])
y = df['income']
sensitive = df['sex']  # 0 = Female, 1 = Male

#  Train-test split  
X_train, X_test, y_train, y_test, sens_train, sens_test = train_test_split(
    X, y, sensitive, test_size=0.2, random_state=42, stratify=y
)


# MODEL 1: BASELINE (no fairness constraint) - for comparison

print("\nTraining BASELINE model (no fairness constraint)")
baseline_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
baseline_model.fit(X_train, y_train)
y_pred_baseline = baseline_model.predict(X_test)

baseline_acc = accuracy_score(y_test, y_pred_baseline)
baseline_dpd = demographic_parity_difference(y_test, y_pred_baseline, sensitive_features=sens_test)
baseline_eod = equalized_odds_difference(y_test, y_pred_baseline, sensitive_features=sens_test)


# MODEL 2: FAIRNESS-CONSTRAINED MODEL

print("Training FAIRNESS-CONSTRAINED model (this takes 2-5 minutes, be patient)")

constraint = DemographicParity()
base_estimator = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)

mitigator = ExponentiatedGradient(
    estimator=base_estimator,
    constraints=constraint,
    eps=0.01          # how strict the fairness constraint is
)

mitigator.fit(X_train, y_train, sensitive_features=sens_train)
y_pred_fair = mitigator.predict(X_test)

fair_acc = accuracy_score(y_test, y_pred_fair)
fair_dpd = demographic_parity_difference(y_test, y_pred_fair, sensitive_features=sens_test)
fair_eod = equalized_odds_difference(y_test, y_pred_fair, sensitive_features=sens_test)


# COMPARISON TABLE

print("\n" + "="*60)
print("BEFORE vs AFTER MITIGATION")
print("="*60)

comparison = pd.DataFrame({
    'Metric': ['Accuracy', 'Demographic Parity Diff', 'Equalized Odds Diff'],
    'Baseline (Before)': [f"{baseline_acc:.4f}", f"{baseline_dpd:.4f}", f"{baseline_eod:.4f}"],
    'Mitigated (After)': [f"{fair_acc:.4f}", f"{fair_dpd:.4f}", f"{fair_eod:.4f}"]
})
print(comparison.to_string(index=False))

#  Selection rates by group, before vs after 
print("\n Selection Rate by Gender: Before ")
mf_before = MetricFrame(metrics=lambda yt, yp: yp.mean(), y_true=y_test, y_pred=y_pred_baseline, sensitive_features=sens_test)
print(mf_before.by_group)

print("\n Selection Rate by Gender: After ")
mf_after = MetricFrame(metrics=lambda yt, yp: yp.mean(), y_true=y_test, y_pred=y_pred_fair, sensitive_features=sens_test)
print(mf_after.by_group)

#  Save comparison for the report 
comparison.to_csv("results/mitigation_comparison.csv", index=False)
print("\nComparison saved to results/mitigation_comparison.csv")

print("\n" + "="*60)
acc_drop = (baseline_acc - fair_acc) * 100
dpd_improvement = (baseline_dpd - fair_dpd) * 100
print(f"TRADEOFF SUMMARY:")
print(f"  Accuracy dropped by:        {acc_drop:.2f} percentage points")
print(f"  Demographic Parity improved by: {dpd_improvement:.2f} percentage points")
print("="*60)