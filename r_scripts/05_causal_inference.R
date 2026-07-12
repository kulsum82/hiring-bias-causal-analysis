
# STEP 3: Causal Inference - Does Gender Cause 
#         the Income Gap? (Propensity Score Matching)


library(tidyverse)
library(MatchIt)
library(cobalt)

# Load clean data
df <- read_csv("data/adult_clean.csv", show_col_types = FALSE)

#  Prepare variables 
df <- df %>%
  mutate(
    income_binary = ifelse(str_trim(income) == ">50K", 1, 0),
    treatment = ifelse(sex == "Female", 1, 0)  # 1 = Female (our "treatment" group)
  ) %>%
  drop_na(workclass, occupation, education_num, hours_per_week, age)

cat("Total rows after cleaning:", nrow(df), "\n")
cat("Female:", sum(df$treatment == 1), " | Male:", sum(df$treatment == 0), "\n")

#  STEP A: Raw (Unmatched) Comparison 
cat("\n=== BEFORE MATCHING (Raw Comparison) ===\n")
raw_comparison <- df %>%
  group_by(treatment) %>%
  summarise(
    pct_high_income = mean(income_binary) * 100,
    avg_education = mean(education_num),
    avg_hours = mean(hours_per_week)
  )
print(raw_comparison)

#  STEP B: Propensity Score Matching 
cat("\nRunning propensity score matching... (this may take 30-60 seconds)\n")

match_model <- matchit(
  treatment ~ age + education_num + hours_per_week + 
              occupation + workclass,
  data = df,
  method = "nearest",
  ratio = 1
)

# Summary of matching quality
summary(match_model)

# Extract matched data
matched_data <- match.data(match_model)

#  STEP C: After Matching Comparison 
cat("\n=== AFTER MATCHING (Fair Comparison) ===\n")
matched_comparison <- matched_data %>%
  group_by(treatment) %>%
  summarise(
    pct_high_income = mean(income_binary) * 100,
    avg_education = mean(education_num),
    avg_hours = mean(hours_per_week)
  )
print(matched_comparison)

# Save matched dataset for the report
write_csv(matched_data, "data/matched_data.csv")
cat("\nMatched dataset saved!\n")