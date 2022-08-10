library(jsonlite)
library(dplyr, warn.conflicts = FALSE)

path <- "data"
path <- list.files(path, pattern = "json", full.names = TRUE)

lawyers <- lapply(path, function(x) as_tibble(fromJSON(x)))
lawyers <- do.call(bind_rows, lawyers)

# 81959 records

group <- c(rep(1:8, each = 10000), rep(9, times = length(links) - 8*10000))
links <- mutate(lawyers["nodealiaspath"], group = group)
links <- split(links, links$group)

links <- lapply(links, function(x) {
  paste0('https://lso.ca', x$nodealiaspath)
})

if (!dir.exists("links")) dir.create("links")

lapply(seq_along(links), function(x) {
  filename <- sprintf("links/link%s.txt", x)
  cat(noquote(links[[x]]), sep = "\n", file = filename)
})
