# ~/utilities/get_cmip6_data/store_data

## Description of the submodule :

It is the submodule dedicated to organize the dictionaries output of the intake-esgf package into more convenient xarray datasets and save them as so.

### dict_netcdf_transform.py

This script is used to go from a dictionnary structure into a series of netcdf files for every single model, variant and experiment. We are able to reload the same structure from the netcdf files. 
To do so, we generate a dataframe associating each entry to its path and save it as a pickle file.
