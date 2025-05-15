#!/usr/bin/env python3

"""
This script is used to perform regridding on a common grid for a bunch of the CMIP6 outputs.
We create a common grid based on the coarser resolutions accessible in the ensemble and transform all the intensive
variables into extensive variables upon regridding thanks to the areacella variable present in the datasets.

Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""

##################################
### IMPORTATION OF THE MODULES ###
##################################

### DATA OBJECTS AND ASSOCIATED COMPUTATION ###

import numpy as np  # to handle numpy arrays and the associated tools

import xarray as xr  # to manage the data

import xcdat as xc  # to handle climate model outputs with xarray

### MATHEMATIC FUNCTIONS ###

from math import floor # to get the int part of a division

### TYPE HINTS FOR FUNCTIONS ###

from numpy.typing import NDArray

#############################################
### GENERATE THE STEPS OF THE COORDINATES ###
#############################################

def get_step(coordinate_array: NDArray[np.float64]) -> float:
    """

    ---

    ### DEFINITION ###

    This function takes a coordinate array and generates its step taking the maximum difference between two grid points.

    ---

    ### INPUTS ###

    COORDINATE_ARRAY : NUMPY ARRAY (NP.FLOAT64) | the array of the coordinates

    ---

    ### OUTPUTS ###

    MAX_STEP : FLOAT | maximum coordinate difference between two grid points

    ---

    """

    max_step = np.max(np.diff(coordinate_array))

    return max_step

####################################################################
### COMPUTE THE CLOSEST STEP THAT DIVIDES THE DOMAIN WITH AN INT ###
####################################################################

def make_a_regular_grid_step(not_regular_step : float, domain_extent : float) -> float :

    """

    ---

    ### DEFINITION ###

    This function takes a coordinate step and the extent of the grid domain in order to compute what would be
    the closest step for making a regular grid. We use the int part of the division domain_extent/step that gives
    us the number of interval the regular step would make and compute it. By definition, the regular step is always
    coarser than the not regular step.

    ---

    ### INPUTS ###

    NOT_REGULAR_STEP : FLOAT | the not regular step (ie) it does not make an int number of intervals

    DOMAIN_EXTENT : FLOAT | the domain extent for the given coordinate

    ---

    ### OUTPUTS ###

    REGULAR_STEP : FLOAT | the step making an int number of intervals of the domain_extent : allowing for a regular grid.

    ---

    """

    ### COMPUTING THE CLOSEST INT NUMBER OF INTERVALS FOR A REGULAR GRID ###

    n_steps_closest = floor(domain_extent / not_regular_step)  # bc we want a step greater than not_regular_step

    ### OBTAIN THE REGULAR_GRID_STEP VALUE ###

    regular_grid_step = domain_extent / n_steps_closest

    return regular_grid_step


##############################################################
### GENERATE THE COARSER STEP FOR A DICTIONARY OF DATASETS ###
##############################################################

def get_coarsest_regular_steps(dict_outputs : dict[str, xr.Dataset]) -> tuple[float, float]:

    """

    ---

    ### DEFINITION ###

    This function gets a dictionary of CMIP6 outputs and generate what would be the coarsest coordinates steps for
    the whole ensemble. It then proceeds to ensure these steps allow for a regular grid (ie) that the extent of the
    grid divided by the step is an integer.

    ---

    ### INPUTS ###

    DICT_OUTPUTS : DICTIONARY OF XR DATASETS | the dictionary holding the models' outputs

    ---

    ### OUTPUTS ###

    (REGULAR_COARSE_STEP_LON, REGULAR_COARSE_STEP_LAT) : TUPLE[FLOAT, FLOAT] | the two coarse step allowing for a regular common grid

    ---

    """

    ### GET THE KEYS OF THE DICTIONARY ###

    list_keys = list(dict_outputs.keys())

    ### GENERATE THE LIST OF COORDINATES ###

    ## Longitude ##

    list_steps_lon = [get_step(dict_outputs[key].lon.values) for key in list_keys]

    ## Latitude ##

    list_steps_lat = [get_step(dict_outputs[key].lat.values) for key in list_keys]

    ### GENERATE THE COARSEST NOT REGULAR STEPS ###

    ## Longitude ##

    max_step_lon = np.max(list_steps_lon)

    ## Latitude ##

    max_step_lat = np.max(list_steps_lat)

    ### CORRECT THEIR VALUES TO MAKE THEM ALLOW FOR A REGULAR GRID ###

    ## Longitude ##

    regular_coarse_step_lon = make_a_regular_grid_step(not_regular_step = max_step_lon, domain_extent = 360)

    ## Latitude ##

    regular_coarse_step_lat = make_a_regular_grid_step(not_regular_step = max_step_lat, domain_extent = 180)

    return  (regular_coarse_step_lon, regular_coarse_step_lat)


#########################################
### GENERATE THE COMMON COARSEST GRID ###
#########################################

def generate_the_common_coarse_grid(dict_outputs : dict[str, xr.Dataset]) -> xr.Dataset:

    """

    ---

    ### DEFINITION ###

    This function gets a dictionary of CMIP6 outputs and generate what is the coarsest common grid on which we can project
    the whole ensemble to loose the least information.

    ---

    ### INPUTS ###

    DICT_OUTPUTS : DICTIONARY OF XR DATASETS | the dictionary holding the models' outputs

    ---

    ### OUTPUTS ###

    COMMON_COARSE_GRID : XARRAY DATASET | the common regular grid on which to project

    ---

    """

    ### GENERATE THE STEPS OF THE GRID ###

    regular_coarse_step_lon, regular_coarse_step_lat = get_coarsest_regular_steps(dict_outputs)

    ### GENERATE THE AXIS ###

    ## Longitude ##

    lon_axis = xc.create_axis("lon", np.arange(0, 360, regular_coarse_step_lon))

    ## Latitude ##

    # since we have picked the step such that the latitude range is divded into an integer number
    # of intervals we may center its bounds on -90 / 90.

    lat_axis = xc.create_axis(
        "lat", np.arange(-90 + regular_coarse_step_lat / 2, 90 + regular_coarse_step_lat / 2, regular_coarse_step_lat)
    )

    ### CREATE THE OUTPUT GRID ###

    common_coarse_grid = xc.create_grid(x = lon_axis, y = lat_axis)

    return common_coarse_grid