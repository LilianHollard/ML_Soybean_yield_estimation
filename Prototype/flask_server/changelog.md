# Changelog
All notable changes to this project will be documented in this file.


The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)


NOTE: This prototype is intended to be reusable by someone, it is not a finished product.
Futhermore, the idea here is to implement tools (back-end serv, python script, ...) front-end is then optional in our case.

## [Unreleased]

### Changed 
- Fixed a bug related to dataframe copy

### Changed - 03-06-2021
- AnneeRef class improved
  - methods related to the modification of the historical dataframe (coeff_prod, year, ...)
## [0.0.2] - 01-06-2021
### Added
- Data form correctly updates the data on the server (pandas dataframe) as well as in the csv files.
- readme.md
- Changelog
### Removed
- images intended for front-end (still viewable from the flask server)

### Added
- Excel file for historical reference year 

## [0.0.1] - 15-05-2021
### Added
-  Python script : historical reference year
-  Flask server
-  Excel file architecture based on the different cities and processed data
-  Usable data form (for historical reference year)
