options(repos = c(CRAN = "https://cloud.r-project.org"))

# Remove any broken V8 installation
if ("V8" %in% rownames(installed.packages())) {
  remove.packages("V8")
}
# Fresh install
install.packages("V8", type = "binary", dependencies = TRUE)

# Verify
if (requireNamespace("V8", quietly = TRUE)) {
  cat("SUCCESS: V8 is now properly installed!\n")
} else {
  cat("FAILED: V8 still not working.\n")
}