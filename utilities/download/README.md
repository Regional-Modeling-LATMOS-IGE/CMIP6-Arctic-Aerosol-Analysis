# Download

This folder contains the downloading and loading routines of the CMIP6 ensemble we use. The intake-esgf package (https://github.com/esgf2-us/intake-esgf?tab=readme-ov-file) is employed to download and load the CMIP6 datasets we need.

## Content

### download_cmip6.ipynb

This notebook shows how we download and load our data for reproducibility. What's more it holds a routine that allows for a fast downloading and loading of the areacella variable for every single downloaded model entry. Indeed, the intake-esgf tends to be quit slow when doing it natively on the large model ensemble we need.

### load_cmip6.py

This python script allows to call the routines introduced in the download_cmip6.ipynb notebook to load the dictionnary variable which holds all of the datasets and the areacella dictionnary associated to it.

### folders_handle

This folder includes functions we use to directly create and clean folders from python for the downloading procedure.

### downloading-environment

This folder holds the conda environment used to run the notebook.

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




