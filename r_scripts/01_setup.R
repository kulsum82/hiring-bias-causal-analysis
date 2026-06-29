# PROJECT: Fairness, Bias & Causal Inference in Hiring/Recruitment Data
# Author : Umme Kulsum
# Date   : 2026
# Installing all the required packages
options(repos = c(CRAN = "https://cloud.r-project.org"))
packages <- c(
  "tidyverse",
  "readr",
  "glm2",
  "lme4",
  "MatchIt",
  "cobalt",
  "dagitty",
  "fairml",
  "ggplot2",
  "ggdag",
  "patchwork",
  "scales",
  "knitr",
  "rmarkdown"
)
installed <- rownames(installed.packages())
to_install <- packages[!packages %in% installed]
if (length(to_install) > 0) {
  cat("Installing", length(to_install), "packages...\n")
  install.packages(to_install, dependencies = TRUE)
} else {
  cat("All packages already installed!\n")
}
lapply(packages, library, character.only = TRUE)
cat("✓ All packages loaded successfully!\n")