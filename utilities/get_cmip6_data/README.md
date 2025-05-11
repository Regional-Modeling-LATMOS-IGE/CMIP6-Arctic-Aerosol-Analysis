# ~/utilities/get_cmip6_data

## Description of the folder :

*get_cmip6_data* is the submodule dedicated to downloading, loading and preparing the needed CMIP6 models' outputs for the analysis.

## Content of the subfolders :

### downloading-environment/

This is the folder that holds the conda environment used to run the notebook.

### folders_handle/

It is the submodule used to manipulate folders with bash methods within python.

### load_raw_data/

This submodule is made to download and load the raw CMIP6 data by using methods described in *get_cmip6_data.ipynb*.

### prepare_data/

This submodule is contributing to the pre-treatment of the datasets produced by the *store_data* submodule before the analysis.

### store_data/

It is the submodule dedicated to organize the dictionaries output of the intake-esgf package into more convenient xarray datasets and save them as so.

## Files present in the folder :

### get_cmip6_data.ipynb

This jupyter notebook is explaining the use of the *intake-esgf* package to download CMIP6 models' output and how we further treat this raw data to turn it into monthly climatologies xarray datasets. It encapsulates the functions coded in *load_raw_data*, *store_data* and *prepare_data*.







