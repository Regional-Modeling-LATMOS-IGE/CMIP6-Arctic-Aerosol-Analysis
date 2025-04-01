# Downloading script's dev branch

Developing a downloading script for the whole CMIP6 data and an example for reproducibility.

## Content of the repository for this branch

The folder */utilities* holds the different scripts used to download and pre-treat the CMIP6 data used for this analysis.\
The notebook held in */utilities/download/* that is named *download_cmip6.ipynb* shows how we use the **intake-esgf** package ([https://github.com/esgf2-us/intake-esgf?tab=readme-ov-file](https://github.com/esgf2-us/intake-esgf)) to download and load the CMIP6 datasets we need. 
What's more, the notebook holds a routine that allows for a fast downloading and loading of the areacella variable for every single downloaded model entry. Indeed, the package tends to be quit slow when doing it natively on the large model ensemble we need.

## Reference of the downloaded data

| activity_drs   | institution_id      | source_id         | experiment_id   | member_id   | table_id   | grid_label   |
|:---------------|:--------------------|:------------------|:----------------|:------------|:-----------|:-------------|
| RFMIP          | CSIRO               | ACCESS-ESM1-5     | piClim-aer      | r1i1p1f1    | Amon       | gn           |
| RFMIP          | CSIRO               | ACCESS-ESM1-5     | piClim-control  | r1i1p1f1    | Amon       | gn           |
| AerChemMIP     | BCC                 | BCC-ESM1          | piClim-control  | r1i1p1f1    | Amon       | gn           |
| AerChemMIP     | BCC                 | BCC-ESM1          | piClim-aer      | r1i1p1f1    | Amon       | gn           |
| RFMIP          | NCAR                | CESM2             | piClim-control  | r1i1p1f1    | Amon       | gn           |
| RFMIP          | NCAR                | CESM2             | piClim-aer      | r1i1p1f1    | Amon       | gn           |
| RFMIP          | CNRM-CERFACS        | CNRM-CM6-1        | piClim-control  | r1i1p1f2    | Amon       | gr           |
| RFMIP          | CNRM-CERFACS        | CNRM-CM6-1        | piClim-aer      | r1i1p1f2    | Amon       | gr           |
| RFMIP          | CNRM-CERFACS        | CNRM-ESM2-1       | piClim-aer      | r1i1p1f2    | Amon       | gr           |
| RFMIP          | CNRM-CERFACS        | CNRM-ESM2-1       | piClim-control  | r1i1p1f2    | Amon       | gr           |
| RFMIP          | CCCma               | CanESM5           | piClim-aer      | r1i1p2f1    | Amon       | gn           |
| RFMIP          | CCCma               | CanESM5           | piClim-control  | r1i1p2f1    | Amon       | gn           |
| RFMIP          | EC-Earth-Consortium | EC-Earth3         | piClim-aer      | r1i1p1f1    | Amon       | gr           |
| RFMIP          | EC-Earth-Consortium | EC-Earth3         | piClim-control  | r1i1p1f1    | Amon       | gr           |
| RFMIP          | NOAA-GFDL           | GFDL-CM4          | piClim-control  | r1i1p1f1    | Amon       | gr1          |
| RFMIP          | NOAA-GFDL           | GFDL-CM4          | piClim-aer      | r1i1p1f1    | Amon       | gr1          |
| RFMIP          | NASA-GISS           | GISS-E2-1-G       | piClim-aer      | r1i1p1f1    | Amon       | gn           |
| RFMIP          | NASA-GISS           | GISS-E2-1-G       | piClim-control  | r1i1p1f1    | Amon       | gn           |
| RFMIP          | IPSL                | IPSL-CM6A-LR      | piClim-aer      | r1i1p1f1    | Amon       | gr           |
| RFMIP          | IPSL                | IPSL-CM6A-LR      | piClim-control  | r1i1p1f1    | Amon       | gr           |
| RFMIP          | IPSL                | IPSL-CM6A-LR-INCA | piClim-aer      | r1i1p1f1    | Amon       | gr           |
| RFMIP          | IPSL                | IPSL-CM6A-LR-INCA | piClim-control  | r1i1p1f1    | Amon       | gr           |
| RFMIP          | MIROC               | MIROC6            | piClim-control  | r1i1p1f1    | Amon       | gn           |
| RFMIP          | MIROC               | MIROC6            | piClim-aer      | r1i1p1f1    | Amon       | gn           |
| RFMIP          | HAMMOZ-Consortium   | MPI-ESM-1-2-HAM   | piClim-control  | r1i1p1f1    | Amon       | gn           |
| RFMIP          | HAMMOZ-Consortium   | MPI-ESM-1-2-HAM   | piClim-aer      | r1i1p1f1    | Amon       | gn           |
| RFMIP          | MRI                 | MRI-ESM2-0        | piClim-control  | r1i1p1f1    | Amon       | gn           |
| RFMIP          | MRI                 | MRI-ESM2-0        | piClim-aer      | r1i1p1f1    | Amon       | gn           |
| RFMIP          | NCC                 | NorESM2-LM        | piClim-aer      | r1i1p1f1    | Amon       | gn           |
| RFMIP          | NCC                 | NorESM2-LM        | piClim-control  | r1i1p1f1    | Amon       | gn           |
| RFMIP          | NCC                 | NorESM2-MM        | piClim-aer      | r1i1p1f1    | Amon       | gn           |
| RFMIP          | NCC                 | NorESM2-MM        | piClim-control  | r1i1p1f1    | Amon       | gn           |
| AerChemMIP     | MOHC                | UKESM1-0-LL       | piClim-control  | r1i1p1f4    | Amon       | gn           |
| AerChemMIP     | MOHC                | UKESM1-0-LL       | piClim-aer      | r1i1p1f4    | Amon       | gn           |




