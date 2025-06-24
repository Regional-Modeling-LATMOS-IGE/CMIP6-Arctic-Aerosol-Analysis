[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# CMIP6-Arctic-Aerosol-Analysis

This repository regroups a bunch of modules and notebooks for a computation of the aerosol-cloud's interaction effective radiative forcing in the Arctic.
This is done using a subset of the CMIP6 model ensemble and using the APRP method devised by *Taylor and al. (2007)* and whose implementation was done by *Zelinka (2023)* (https://zenodo.org/records/8206763).

## References : 

### APRP method theory and use

- Taylor, K. E. et al. (2007), [Estimating shortwave radiative forcing and response in climate models](https://journals.ametsoc.org/doi/10.1175/JCLI4143.1), J. Clim., 20(11), 2530-2543, doi:10.1175/JCLI4143.1.

- Zelinka, M. D., T. Andrews, P. M. Forster, and K. E. Taylor, 2014: [Quantifying Components of Aerosol-Cloud-Radiation Interactions in Climate Models](http://onlinelibrary.wiley.com/doi/10.1002/2014JD021710/abstract), _J. Geophys. Res._, 119, 7599-7615, doi:10.1002/2014JD021710.

### APRP module used for our analysis

- https://zenodo.org/records/8206763

- Zelinka, M. D., Smith, C. J., Qin, Y., and Taylor, K. E.: [Comparison of methods to estimate aerosol effective radiative forcings in climate models](https://acp.copernicus.org/articles/23/8879/2023/), Atmos. Chem. Phys., 23, 8879–8898, https://doi.org/10.5194/acp-23-8879-2023, 2023. 

## Content of the subfolders :

### utilities/

The utilities module is used for the analysis. It holds different submodules used through the different jupyter notebooks.

### environment/

The environment folder is useful if you wish to replicate my work. It holds the conda environment holding all the dependencies of the repository.

## Notebooks present in this folder :

### get_cmip6_data.ipynb

This jupyter notebook is explaining the use of the *intake-esgf* package to download CMIP6 models' output and how we further treat this raw data to turn it into monthly climatologies xarray datasets. It encapsulates the functions coded in *folders_handle*, *load_raw_data*, *store_data* and *prepare_data*.

### demonstrate_reproducibility_of_zelinkas_results.ipynb

This jupyter notebook aims at showing that our scripts are reproducing the results found in [Comparison of methods to estimate aerosol effective radiative forcings in climate models](https://acp.copernicus.org/articles/23/8879/2023/).

### sw_analysis_aprp_arctic.ipynb

This jupyter notebook is my current work notebook. It is expected to be messier than the rest of the notebook as I'm making progress from what I'm coding there. Its goal is to explore the results induced by the APRP method and develop my own methods.

### bar_plots_of_aprp.ipynb

This jupyter notebook exhibits some of our APRP products in the Arctic through bar plots. It is handful to show the ensemble spread.

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
| 13 | IPSL-CM6A-LR      | r2i1p1f1    | gr           |
| 14 | IPSL-CM6A-LR      | r3i1p1f1    | gr           |
| 15 | IPSL-CM6A-LR      | r4i1p1f1    | gr           |
| 16 | IPSL-CM6A-LR-INCA | r1i1p1f1    | gr           |
| 17 | MIROC6            | r11i1p1f1   | gn           |
| 18 | MIROC6            | r1i1p1f1    | gn           |
| 19 | MPI-ESM-1-2-HAM   | r1i1p1f1    | gn           |
| 20 | MRI-ESM2-0        | r1i1p1f1    | gn           |
| 21 | NorESM2-LM        | r1i1p2f1    | gn           |
| 22 | NorESM2-LM        | r1i1p1f1    | gn           |
| 23 | NorESM2-MM        | r1i1p1f1    | gn           |
| 24 | UKESM1-0-LL       | r1i1p1f4    | gn           |

## Packages needed :

The packages needed can be accessed with *conda*. The conda environment export can be retrieved from */utilities/environment/*.
