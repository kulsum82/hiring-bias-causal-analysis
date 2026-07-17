# Fairness, Bias & Causal Inference in Hiring/Income Prediction
## [View interactive dashboard](results/dashboard.html)

> A combined R and Python research project investigating gender-based income disparity through descriptive statistics, causal inference, and machine learning fairness analysis.

---

##  Project Overview

This project examines whether gender-based income disparity in U.S. census employment data is:
1. **Statistically significant** (is the gap real, or random chance?)
2. **Causally persistent** (does it survive after controlling for education, occupation, hours worked?)
3. **Reproduced by ML models** (do algorithms trained on this data inherit the same bias?)
4. **Reducible through fairness constraints** (can we fix it, and at what cost?)

**Key Finding:** A ~20 percentage point gender income gap persists after propensity score matching on all major confounders (p < 2.2×10⁻¹⁶), is reproduced by a Random Forest classifier, and can be reduced by 96% using fairness-constrained learning - but only at the cost of increasing equalized odds disparity, illustrating the well-documented **impossibility of simultaneously satisfying multiple fairness criteria**.

---

##  Dataset

**UCI Adult Income Dataset** - 32,561 records from the 1994 U.S. Census Bureau

| Feature | Description |
|---|---|
| `age` | Continuous |
| `education_num` | Years of education (numeric) |
| `occupation` | Job category |
| `hours_per_week` | Weekly working hours |
| `sex` | Gender (Male/Female) |
| `race` | Race category |
| `income` | Target: ≤$50K or >$50K |

Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/2/adult)

---

##  Methodology & Results

### Step 1: Exploratory Data Analysis (R)

Raw income distribution by gender revealed a substantial disparity:

| Gender | ≤$50K | >$50K |
|--------|-------|-------|
| Female | 89.1% | **10.9%** |
| Male | 69.4% | **30.6%** |

**Raw gap: 19.7 percentage points** - men nearly 3× more likely to earn >$50K.

A secondary racial disparity was also identified: White and Asian-Pac-Islander groups earned >$50K at ~26-27%, compared to ~9-12% for Black, Amer-Indian-Eskimo, and Other groups.

---

### Step 2: Causal Inference - Propensity Score Matching (R)

**Question:** Is the gap simply explained by women having different jobs, education, or working hours?

**Method:** Propensity Score Matching (nearest-neighbor, 1:1) on:
- Age
- Education level (numeric)
- Hours worked per week
- Occupation
- Workclass

**Result:** 9,930 matched male-female pairs with nearly identical covariates (avg. education: 10.1F vs 10.5M; avg. hours: 37.0F vs 39.5M)

| | Raw Comparison | After Matching |
|---|---|---|
| Male >$50K | 30.6% | 31.4% |
| Female >$50K | 10.9% | 11.3% |
| **Gap** | **19.7 pts** | **20.1 pts** |

**The gap did not shrink** - it persisted virtually unchanged after controlling for all observable confounders.

**Statistical Significance Test** (Two-Proportion Z-Test on matched data):
- χ² = 1185.5, df = 1
- **p-value < 2.2 × 10⁻¹⁶**
- **95% CI: [18.9%, 21.2%]**

---

### Step 3: Machine Learning Fairness Analysis (Python)

**Model:** Random Forest Classifier (100 trees, max depth 10)

| Metric | Value |
|---|---|
| Overall Accuracy | 85.25% |
| Precision (>$50K) | 0.80 |
| Recall (>$50K) | 0.55 |
| F1-score (>$50K) | 0.65 |

**Fairness Breakdown by Gender:**

| Group | Selection Rate (predicted >$50K) | Accuracy |
|---|---|---|
| Female | 7.3% | 92.6% |
| Male | 21.8% | 81.7% |

**Fairness Metrics:**
- Demographic Parity Difference: **0.145** (0 = fair)
- Equalized Odds Difference: **0.062** (0 = fair)

The model predicted high income for men ~3× more often than women, reproducing the real-world disparity found in Steps 1 and 2.

---

### Step 4: Bias Mitigation (Python + Fairlearn)

**Method:** Exponentiated Gradient with Demographic Parity constraint (ε = 0.01)

| Metric | Before Mitigation | After Mitigation | Change |
|---|---|---|---|
| Accuracy | 85.25% | 83.84% | -1.41 pts |
| Demographic Parity Diff | 0.145 | **0.0053** | **-96% ** |
| Equalized Odds Diff | 0.062 | **0.285** | +360%  |

| Selection Rate | Before | After |
|---|---|---|
| Female | 7.3% | 16.0% |
| Male | 21.8% | 16.5% |

**Key Insight - The Fairness Impossibility Theorem in Practice:**
Mitigation nearly eliminated demographic parity disparity (7.3% → 16.0% for women) at a modest accuracy cost of 1.41 points. However, equalized odds disparity increased 4× — demonstrating empirically that when base rates differ between groups, no classifier can simultaneously satisfy both demographic parity and equalized odds (Kleinberg et al., 2016; Chouldechova, 2017).

---

##  Repository Structure

```
hiring-bias-causal-analysis/
│
├── data/
│   ├── adult_clean.csv              # Cleaned dataset (downloaded once)
│   ├── matched_data.csv             # Propensity score matched dataset
│   └── model_predictions.csv        # ML model predictions for fairness analysis
│
├── r_scripts/
│   ├── 01_setup.R                   # Install & load all R packages
│   ├── 03_load_data.R               # Download & clean the UCI dataset
│   ├── 04_eda_visuals.R             # Income by gender & race charts
│   ├── 05_causal_inference.R        # Propensity score matching
│   └── 06_significance_test.R       # Two-proportion z-test & chi-square
│
├── python_scripts/
│   ├── 01_train_model.py            # Train Random Forest classifier
│   ├── 02_fairness_metrics.py       # Measure bias with Fairlearn
│   └── 03_bias_mitigation.py        # Fairness-constrained retraining
│
├── results/
│   ├── 01_income_by_gender.png      # Gender income disparity chart
│   ├── 02_income_by_race.png        # Race income disparity chart
│   └── mitigation_comparison.csv    # Before/after mitigation table
│
├── .gitignore
└── README.md
```

---

##  How to Reproduce

### Prerequisites

- R 4.5+
- Python 3.13+
- Git

### Step 1 - Clone the Repository

```bash
git clone https://github.com/kulsum82/hiring-bias-causal-analysis.git
cd hiring-bias-causal-analysis
```

### Step 2 - Set Up R Environment

```bash
Rscript r_scripts/01_setup.R
```

This installs all required R packages automatically.

### Step 3 - Load & Explore the Data

```bash
Rscript r_scripts/03_load_data.R
Rscript r_scripts/04_eda_visuals.R
```

### Step 4 - Run Causal Inference

```bash
Rscript r_scripts/05_causal_inference.R
Rscript r_scripts/06_significance_test.R
```

### Step 5 - Set Up Python Environment

```bash
pip install pandas numpy matplotlib seaborn scikit-learn fairlearn
```

### Step 6 — Run ML Fairness Analysis

```bash
py python_scripts/01_train_model.py
py python_scripts/02_fairness_metrics.py
py python_scripts/03_bias_mitigation.py
```

---

## References

- Kleinberg, J., Mullainathan, S., & Raghavan, M. (2016). *Inherent Trade-Offs in the Fair Determination of Risk Scores.*
- Chouldechova, A. (2017). *Fair Prediction with Disparate Impact.*
- Dwork, C. et al. (2012). *Fairness Through Awareness.*
- Agarwal, A. et al. (2018). *A Reductions Approach to Fair Classification.* (Exponentiated Gradient)
- Dua, D. and Graff, C. (2019). *UCI ML Repository: Adult Data Set.*

---
