# Combine, filter, and sort data from multiple CSV
library(dplyr, warn.conflicts = FALSE)

files <- list.files("results", pattern = ".csv", full.names = TRUE)
csv <- lapply(files, read.csv)
csv <- do.call(bind_rows, csv)
csv <- as_tibble(csv)

csv <- csv %>% 
  select(
    Full.Name, # Full name
    Fist.Name, # First name
    Last.Name, # Last name
    Business.Name, # Organization/Firm Name
    Email.Address, # Email
    Status, # Status
    Area.s..of.Law.Legal.Services, # Area of Law Address
    Phone, # Phone #
    Fax, # Fax #
    Class.of.Licence, # Class of Licence
    Real.Estate.Insured, # Real Estate Insured
    Trusteeships, # Trusteeships
    Current.Practice.Restrictions, # Current Practice Restrictions
    Current.Regulatory.Proceedings, # Current Regulatory Proceedings
    Link # Link to page
  ) %>% arrange(Last.Name, Fist.Name) # Yes, typo! Should be First

header <- c(
  "Full name",
  "First name",
  "Last name",
  "Organization/Firm Name",
  "Email",
  "Status",
  "Area of Law Address",
  "Phone Number",
  "Fax Number",
  "Class of Licence",
  "Real Estate Insured",
  "Trusteeships",
  "Current Practice Restrictions",
  "Current Regulatory Proceedings",
  "Link to page"
)

names(csv) <- header

if (!dir.exists("data")) dir.create("data")
write.csv(csv, file = "data/data.csv", na = "", row.names = FALSE)
