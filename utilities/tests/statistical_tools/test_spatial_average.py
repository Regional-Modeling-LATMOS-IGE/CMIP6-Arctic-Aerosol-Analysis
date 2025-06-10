#!/usr/bin/env python3

"""
Test library for spatial_average.py

Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""


### MODULE TO BE TESTED ###

from utilities.tools_for_analysis.statistical_tools.spatial_average import (
    adapt_for_spatial_avgd, # to adapt the dataset attributes for spatial average
    spatial_average_given_field, # to realize the spatial average of a given field
)


### DATA OBJECTS AND ASSOCIATED COMPUTATION ###

import xarray as xr  # to manage the data

import numpy as np # to handle numpy arrays and the associated tools

### TEST MODULE ###

import pytest

#########################################
### TESTS FOR ADAPT_FOR_SPATIAL_AVGD ###
#########################################

### DEFINE TEST ARRAY ###

test1 = xr.Dataset(

    data_vars=dict(

        test=(["lon", "lat"], np.array([[0]])),

    ),

    coords=dict(

        lon=("loc", [0]),

        lat=("loc", [0]),
    ),

    attrs=dict(description="Test dataset 1"),

)

### TESTS ###

def test_attribute_latitude():
    assert adapt_for_spatial_avgd(test1).lat.attrs["axis"] == 'Y'


def test_attribute_longitude():
    assert adapt_for_spatial_avgd(test1).lon.attrs["axis"] == 'X'


#############################################
### TESTS FOR SPATIAL_AVERAGE_GIVEN_FIELD ###
#############################################

### DEFINE TEST XARRAY ###

test_map =  np.array([[2, 1, 2], [1, 0, 1], [2, 1, 2]])
                     
arr = xr.DataArray(

    data= test_map,

    dims=["lon", "lat"],

    coords={"lon": range(3), "lat": range(3)},

    attrs=dict(description="Test dataset 2"),

)

test2 = xr.Dataset({"test": arr})

### TESTS ###

def test_not_adapted_for_spatial_average_given_field():
    with pytest.raises(KeyError):

        spatial_average_given_field(
            field = "test",
            dataset = test2
        )


test3 = adapt_for_spatial_avgd(test2) # need another name here because pytest defines everything before running tests

def test_good_result_average_spatial_average_given_field():
    assert spatial_average_given_field(field = "test", dataset = test3) == np.round(np.mean(test_map),2)

