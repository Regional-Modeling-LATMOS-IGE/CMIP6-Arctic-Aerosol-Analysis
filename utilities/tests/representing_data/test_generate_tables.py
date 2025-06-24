#!/usr/bin/env python3

"""
Test library for generate_tables.py.

Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""


### MODULE TO BE TESTED ###

from utilities.representing_data.generate_tables import (
    compute_needed_spatial_avg_for_tables,  # to generate the table's rows for each key
)


### DATA OBJECTS AND ASSOCIATED COMPUTATION ###

import xarray as xr  # to manage the data

import numpy as np  # to handle numpy arrays and the associated tools

### HOMEMADE LIBRARIES ###

from utilities.tools_for_analysis.statistical_tools.spatial_average import (
    adapt_for_spatial_avgd,  # to adapt the dataset attributes for spatial average
)

### TEST MODULE ###

import pytest

#######################################################
### TESTS FOR COMPUTE_NEEDED_SPATIAL_AVG_FOR_TABLES ###
#######################################################

### DEFINE TEST XARRAY ###

test_map = np.array([[2, 1, 2], [1, 0, 1], [2, 1, 2]])

arr = xr.DataArray(
    data=[test_map, test_map],
    dims=["time", "lon", "lat"],
    coords={"time": range(2), "lon": range(3), "lat": range(3)},
    attrs=dict(description="Test dataset"),
)

test = xr.Dataset({"noncld_scat": arr})

## To compute spatial average on this made up dataset ##

test = adapt_for_spatial_avgd(test)

### TESTS ###


def test_error_if_wrong_type_first_input_compute_needed_spatial_avg_for_tables():
    with pytest.raises(TypeError):
        compute_needed_spatial_avg_for_tables(key=3, dataset=test)


def test_error_if_dataset_not_averaged_over_time_input_compute_needed_spatial_avg_for_tables():
    with pytest.raises(
        ValueError,
        match="The size of the spatially averaged values needs to be one. Check if the input dataset has undergone a time average.",
    ):
        compute_needed_spatial_avg_for_tables(key="test", dataset=test)
