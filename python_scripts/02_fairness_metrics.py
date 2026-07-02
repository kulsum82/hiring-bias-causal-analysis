
# STEP 4B: Measure Bias Using Fairlearn

import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, precision_score
from fairlearn.metrics import (
    MetricFrame,
    demographic_parity_difference,
    equalized_odds_difference
)

print("Loading model predictions")

# Load the predictions saved from the previous script
results = pd.read_csv("data/model_predictions.csv")

y_true = results['y_true']
y_pred = results['y_pred']
sensitive_sex = results['sex']  # 0/1 encoded gender

print(f"\nTotal test samples: {len(results)}")
print(f"Sensitive feature 'sex' values: {sensitive_sex.unique()}")

# ---- Overall accuracy ----
overall_acc = accuracy_score(y_true, y_pred)
print(f"\nOverall model accuracy: {overall_acc:.4f}")

# ---- Breakdown by gender using MetricFrame ----
print("\n Performance Breakdown by Gender ")
metric_frame = MetricFrame(
    metrics={
        'accuracy': accuracy_score,
        'selection_rate': lambda yt, yp: yp.mean(),  # % predicted as >50K
        'recall': recall_score,
        'precision': precision_score
    },
    y_true=y_true,
    y_pred=y_pred,
    sensitive_features=sensitive_sex
)
print(metric_frame.by_group)

# ---- Key Fairness Metrics ----
print("\n Fairness Metrics ")

dpd = demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive_sex)
print(f"Demographic Parity Difference: {dpd:.4f}")
print("  (0 = perfectly fair, higher = more biased)")

eod = equalized_odds_difference(y_true, y_pred, sensitive_features=sensitive_sex)
print(f"Equalized Odds Difference: {eod:.4f}")
print("  (0 = perfectly fair, higher = more biased)")

# ---- Compare model bias to raw data bias ----
print("\n Comparison: Raw Data vs Model Predictions ")
selection_rates = metric_frame.by_group['selection_rate']
print(f"Model predicts >50K for group 0 (likely Male):   {selection_rates.iloc[0]*100:.1f}%")
print(f"Model predicts >50K for group 1 (likely Female): {selection_rates.iloc[1]*100:.1f}%")
gap = abs(selection_rates.iloc[0] - selection_rates.iloc[1]) * 100
print(f"Model's gender gap in predictions: {gap:.1f} percentage points")
print(f"(Compare this to your R finding: 20.1 percentage points)")
