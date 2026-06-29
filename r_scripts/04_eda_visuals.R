# ============================================
# STEP 2 (Part 2): Exploratory Visualizations
# ============================================

library(tidyverse)

# Load the clean dataset
df <- read_csv("data/adult_clean.csv", show_col_types = FALSE)

# Clean up income column (remove extra spaces if any)
df <- df %>% mutate(income = str_trim(income))

# ---- Chart 1: Income distribution by Gender ----
p1 <- df %>%
  count(sex, income) %>%
  group_by(sex) %>%
  mutate(pct = n / sum(n) * 100) %>%
  ggplot(aes(x = sex, y = pct, fill = income)) +
  geom_col(position = "dodge") +
  labs(
    title = "Income Distribution by Gender",
    x = "Gender", y = "Percentage (%)", fill = "Income Level"
  ) +
  theme_minimal()

ggsave("results/01_income_by_gender.png", p1, width = 7, height = 5)
print(p1)

# ---- Chart 2: Income distribution by Race ----
p2 <- df %>%
  count(race, income) %>%
  group_by(race) %>%
  mutate(pct = n / sum(n) * 100) %>%
  ggplot(aes(x = race, y = pct, fill = income)) +
  geom_col(position = "dodge") +
  labs(
    title = "Income Distribution by Race",
    x = "Race", y = "Percentage (%)", fill = "Income Level"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

ggsave("results/02_income_by_race.png", p2, width = 8, height = 5)
print(p2)

# ---- Quick numeric summary ----
cat("\n--- Income % by Gender ---\n")
df %>%
  count(sex, income) %>%
  group_by(sex) %>%
  mutate(pct = round(n / sum(n) * 100, 1)) %>%
  print()

cat("\nCharts saved in results/ folder!\n")