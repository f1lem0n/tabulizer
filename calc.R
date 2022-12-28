# install.packages("reticulate")
library(reticulate)
library(ggplot2)

# source for variables
reticulate::source_python(file = "run.py")

var_list <- py$var_list

headers <- list()
data_sets <- list()
for (var in var_list) {
    headers <- append(headers, var$header, length(headers))
    data_sets <- append(data_sets, list(var$data), length(headers))
}

df <- data.frame(data_sets)
colnames(df) <- headers
print(df)
