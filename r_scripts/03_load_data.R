
# STEP   : Load & Explore the Dataset
# Dataset: UCI Adult Income (Census) Data


library(tidyverse)

# Download the dataset
url <- "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
destination <- "data/adult_raw.csv"

if (!file.exists(destination)) {
  download.file(url, destfile = destination, mode = "wb")
  cat("Dataset downloaded successfully!\n")
} else {
  cat("Dataset already exists locally — skipping download.\n")
}

# Define column names
col_names <- c(
  "age", "workclass", "fnlwgt", "education", "education_num",
  "marital_status", "occupation", "relationship", "race", "sex",
  "capital_gain", "capital_loss", "hours_per_week", "native_country",
  "income"
)

# Read the CSV into R
df <- read_csv(
  destination,
  col_names = col_names,
  na = "?",
  trim_ws = TRUE,
  show_col_types = FALSE
)

cat("\nDataset loaded! Dimensions:\n")
print(dim(df))

# Quick look at the data
cat("\nFirst 5 rows:\n")
print(head(df, 5))

cat("\nColumn structure:\n")
glimpse(df)

# Check for missing values
cat("\nMissing values per column:\n")
print(colSums(is.na(df)))

# Save cleaned version for later use
write_csv(df, "data/adult_clean.csv")
cat("\nClean dataset saved to data/adult_clean.csv\n")