# Data check up: duplication, failed scraped
library(dplyr, warn.conflicts = FALSE)

source("combine.R")

# Paralegal give an empty, we should to fill them
csv <- csv %>% 
  mutate(`Class of Licence` = ifelse(`Class of Licence` == "", "Paralegal", `Class of Licence`))
write.csv(csv, file = "data/data.csv", na = "", row.names = FALSE)

# Get failed link
link_scraped <- csv$`Link to page`
link_avail <- tolower(read.csv("all-links.txt", header = FALSE)[[1]])
link_addition <- link_avail[!(link_avail %in% link_scraped)]
filename <- "links/failed_links.txt"
cat(noquote(link_addition), sep = "\n", file = filename)
