#!/usr/bin/env python3

"""
This submodule holds the routines that allow to realize spatial averages of the dictionary data.
Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""

###################################
### IMPORTATIONS OF THE MODULES ###
###################################

### DATA OBJECTS AND ASSOCIATED COMPUTATION ###

import numpy as np  # to handle numpy arrays and the associated tools

import xarray as xr  # to manage the data

import xcdat as xc  # to handle climate model outputs with xarray

### TYPE HINTS FOR FUNCTIONS ###

from numpy.typing import NDArray  # type hints for numpy

###############################################################
### ADAPT THE ARRAYS FOR DOING A SPATIAL AVERAGE WITH XCDAT ###
###############################################################

def adapt_for_spatial_avgd(dataset : xr.Dataset) -> xr.Dataset :

    """

    ---

    ### DEFINITION ###

    This function changes the attributes of the axes in a dataset. This is mandatory to use the spatial averaging techniques of xcdat.

    ---

    ### INPUTS ###

    DATASET : XR DATASET | dataset that will get its attributes changed

    ---

    ### OUTPUTS ###

    DATASET : XR.DATASET | dataset with its attributes changed

    ---
    """

    ### CHANGE THE ATTRIBUTES OF THE AXES OF DATASET ###

    ## LATITUDE ##

    dataset.lat.attrs["axis"] = "Y"

    ## LONGITUDE ##

    dataset.lon.attrs["axis"] = "X"

    ## SET BOUNDS ##

    dataset = dataset.bounds.add_missing_bounds()

    return dataset

########################################
### SPATIAL AVERAGE OF A GIVEN FIELD ###
########################################

def spatial_average_given_field(field : str, dataset : xr.Dataset) -> NDArray[np.float64]:

    """

    ---

    ### DEFINITION ###

    This function changes computes the spatial average of a provided input field on a given dataset.

    ---

    ### INPUTS ###

    FIELD : STR | field to be averaged 

    DATASET : XR DATASET | dataset holding the variable to average

    ---

    ### OUTPUTS ###

    SPATIAL_AVG : NUMPY ARRAY OF FLOAT 64 | the spatial average of the dataset fields.Its dimensions depends of the time dimension of the dataset.

    ---
    """

    ### COMPUTE THE SPATIAL AVERAGE ###

    ## Generate the spatial average ##

    spatial_avg = dataset.spatial.average(field, axis=["X", "Y"])[field].values

    ## Round it to 2 digits after the comma ##

    spatial_avg = np.round(spatial_avg, 2)

    return spatial_avg
