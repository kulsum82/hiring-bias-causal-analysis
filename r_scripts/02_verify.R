cat("Checking all packages \n\n")
check = function(pkg){
    if (requireNamespace(pkg, quietly = TRUE)) {
        cat("YES",pkg,"\n")
    }   else {
        cat("MISSING: ", pkg, "\n")
    }
}

check("tidyverse")
check("MatchIt")
check("dagitty")
check("ggdag")
check("fairml")
check("cobalt")
cat("\nIf any show NO , tell me and we'll fix it!\n")
