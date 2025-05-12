[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# CMIP6-Arctic-Aerosol-Analysis

## utilities/ 

The utilities module is used for the analysis. It holds different submodules explained through jupyter notebooks present on the same path.

## Notebooks present in this folder :

### get_cmip6_data.ipynb

This jupyter notebook is explaining the use of the *intake-esgf* package to download CMIP6 models' output and how we further treat this raw data to turn it into monthly climatologies xarray datasets. It encapsulates the functions coded in *folders_handle*, *load_raw_data*, *store_data* and *prepare_data*.

## Models' outputs used for both experiments :

|    | source_id         | member_id   | grid_label   |
|---:|:------------------|:------------|:-------------|
|  0 | ACCESS-CM2        | r1i1p1f1    | gn           |
|  1 | ACCESS-ESM1-5     | r1i1p1f1    | gn           |
|  2 | BCC-ESM1          | r1i1p1f1    | gn           |
|  3 | CESM2             | r1i1p1f1    | gn           |
|  4 | CNRM-CM6-1        | r1i1p1f2    | gr           |
|  5 | CNRM-ESM2-1       | r1i1p1f2    | gr           |
|  6 | CanESM5           | r1i1p2f1    | gn           |
|  7 | GFDL-CM4          | r1i1p1f1    | gr1          |
|  8 | GISS-E2-1-G       | r1i1p1f1    | gn           |
|  9 | GISS-E2-1-G       | r1i1p1f2    | gn           |
| 10 | GISS-E2-1-G       | r1i1p3f1    | gn           |
| 11 | HadGEM3-GC31-LL   | r1i1p1f3    | gn           |
| 12 | IPSL-CM6A-LR      | r1i1p1f1    | gr           |
| 13 | IPSL-CM6A-LR      | r3i1p1f1    | gr           |
| 14 | IPSL-CM6A-LR      | r4i1p1f1    | gr           |
| 15 | IPSL-CM6A-LR      | r2i1p1f1    | gr           |
| 16 | IPSL-CM6A-LR-INCA | r1i1p1f1    | gr           |
| 17 | MIROC6            | r11i1p1f1   | gn           |
| 18 | MIROC6            | r1i1p1f1    | gn           |
| 19 | MPI-ESM-1-2-HAM   | r1i1p1f1    | gn           |
| 20 | MRI-ESM2-0        | r1i1p1f1    | gn           |
| 21 | NorESM2-LM        | r1i1p2f1    | gn           |
| 22 | NorESM2-LM        | r1i1p1f1    | gn           |
| 23 | NorESM2-MM        | r1i1p1f1    | gn           |
| 24 | UKESM1-0-LL       | r1i1p1f4    | gn           |
