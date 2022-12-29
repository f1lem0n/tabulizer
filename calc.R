# install.packages("reticulate")
library(reticulate)
library(ggplot2)

# setting variable sources
reticulate::source_python(file = "reader.py")
args = commandArgs(trailingOnly=TRUE)

# making a dataframe
headers <- list()
data_sets <- list()
for (var in var_list) {
    headers <- append(headers, var$header, length(headers))
    data_sets <- append(data_sets, list(var$data), length(headers))
}
df <- data.frame(data_sets)
colnames(df) <- headers



quit()
