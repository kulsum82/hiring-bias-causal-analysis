
# STEP 3B: Statistical Significance Test
# Is the matched income gap statistically real?


library(tidyverse)

# Load the matched dataset from Step 3
matched_data <- read_csv("data/matched_data.csv", show_col_types = FALSE)

cat("=== Two-Proportion Z-Test ===\n")
cat("H0 (Null Hypothesis): Income rate is the SAME for men and women\n")
cat("H1 (Alternative): Income rate is DIFFERENT for men and women\n\n")

# Count successes (high income) and totals per group
summary_counts <- matched_data %>%
  group_by(treatment) %>%
  summarise(
    n_high_income = sum(income_binary),
    total = n()
  )
print(summary_counts)

# Extract values for the test
x_male   <- summary_counts$n_high_income[summary_counts$treatment == 0]
x_female <- summary_counts$n_high_income[summary_counts$treatment == 1]
n_male   <- summary_counts$total[summary_counts$treatment == 0]
n_female <- summary_counts$total[summary_counts$treatment == 1]

# Run the two-proportion z-test (prop.test)
test_result <- prop.test(
  x = c(x_male, x_female),
  n = c(n_male, n_female),
  alternative = "two.sided",
  correct = TRUE
)

cat("\n=== Test Results ===\n")
print(test_result)

# Interpret it clearly
cat("\n=== Interpretation ===\n")
p_val <- test_result$p.value
if (p_val < 0.001) {
  cat("p-value < 0.001 — The gap is HIGHLY statistically significant.\n")
} else if (p_val < 0.05) {
  cat("p-value =", round(p_val, 5), "— The gap IS statistically significant (p < 0.05).\n")
} else {
  cat("p-value =", round(p_val, 5), "— The gap is NOT statistically significant.\n")
}

cat("\n95% Confidence Interval for the difference in proportions:\n")
print(test_result$conf.int)

#  Bonus: Chi-square test (alternative method, same conclusion) 
cat("\n=== Chi-Square Test (cross-check) ===\n")
contingency_table <- table(matched_data$treatment, matched_data$income_binary)
print(contingency_table)
chi_result <- chisq.test(contingency_table)
print(chi_result)