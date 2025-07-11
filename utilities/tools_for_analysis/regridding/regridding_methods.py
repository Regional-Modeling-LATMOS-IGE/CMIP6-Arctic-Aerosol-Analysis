#!/usr/bin/env python3

"""
This script is used to perform regridding on a common grid for a bunch of the CMIP6 outputs.

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

from math import floor  # to get the int part of a division

### TO DISPLAY A PROGRESS BAR ###

from tqdm import tqdm  # progress bar handler

### TYPE HINTS FOR FUNCTIONS ###

from numpy.typing import NDArray  # type hints for numpy

### HOMEMADE LIBRARIES ###

## Handle the climatology dictionary ##

from utilities.get_cmip6_data.prepare_data.extract_climatologies import (
    add_one_variable_to_dataset,  # to add one variable to the full dataset
)

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


def make_a_regular_grid_step(not_regular_step: float, domain_extent: float) -> float:
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

    n_steps_closest = floor(
        domain_extent / not_regular_step
    )  # bc we want a step greater than not_regular_step

    ### OBTAIN THE REGULAR_GRID_STEP VALUE ###

    regular_grid_step = domain_extent / n_steps_closest

    return regular_grid_step


##############################################################
### GENERATE THE COARSER STEP FOR A DICTIONARY OF DATASETS ###
##############################################################


def get_coarsest_regular_steps(
    dict_outputs: dict[str, xr.Dataset],
) -> tuple[float, float]:
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

    regular_coarse_step_lon = make_a_regular_grid_step(
        not_regular_step=max_step_lon, domain_extent=360
    )

    ## Latitude ##

    regular_coarse_step_lat = make_a_regular_grid_step(
        not_regular_step=max_step_lat, domain_extent=180
    )

    return (regular_coarse_step_lon, regular_coarse_step_lat)


#########################################
### GENERATE THE COMMON COARSEST GRID ###
#########################################


def generate_the_common_coarse_grid(dict_outputs: dict[str, xr.Dataset]) -> xr.Dataset:
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

    regular_coarse_step_lon, regular_coarse_step_lat = get_coarsest_regular_steps(
        dict_outputs
    )

    ### GENERATE THE AXIS ###

    ## Longitude ##

    lon_axis = xc.create_axis("lon", np.arange(0, 360, regular_coarse_step_lon))

    ## Latitude ##

    # since we have picked the step such that the latitude range is divded into an integer number
    # of intervals we may center its bounds on -90 / 90.

    lat_axis = xc.create_axis(
        "lat",
        np.arange(
            -90 + regular_coarse_step_lat / 2,
            90 + regular_coarse_step_lat / 2,
            regular_coarse_step_lat,
        ),
    )

    ### CREATE THE OUTPUT GRID ###

    common_coarse_grid = xc.create_grid(x=lon_axis, y=lat_axis)

    return common_coarse_grid


#######################################################
### COMPUTE THE AREACELLA VARIABLE FOR A GIVEN GRID ###
#######################################################


def compute_grid_areacella(
    grid: xr.Dataset, verbose: bool = False
) -> NDArray[np.float64]:
    """

    ---

    ### DEFINITION ###

    This function takes as an input a 2D grid and generates the area for every grid cell. The result will be
    a map holding the area for every grid point.

    ---

    ### INPUTS ###

    GRID : XR DATASET | the dictionary holding the models' outputs

    VERBOSE : BOOL | do we display the steps of the grid ?

    ---

    ### OUTPUTS ###

    AREACELLA : NDArray[np.float64] | the areacella variable on the 2D grid given as an input
    ---

    """
    ### INITIALIZATION ###

    ## Define the radius of the earth ##

    R_earth = 6371.0 * 10**3  # in m

    ## Define the lat and lon arrays ##

    latitude = grid.lat

    longitude = grid.lon

    ## Define the steps in radians ##

    # In degreees #

    dlon = np.mean(np.diff(longitude))

    dlat = np.mean(np.diff(latitude))

    # In rad #

    dlon_rad = np.deg2rad(dlon)

    dlat_rad = np.deg2rad(dlat)

    if verbose:

        print(dlon, dlat)

    ## Define the shape of the grid ##

    n_lat = grid.lat.size

    n_lon = grid.lon.size

    ### COMPUTATION OF AREACELLA FOR ONE MODEL ###

    ## Definition ##

    areacella = np.zeros((n_lat, n_lon))

    ## Cycle for ##

    for ii_lat, lat in enumerate(latitude):

        for ii_lon, lon in enumerate(longitude):

            areacella[ii_lat, ii_lon] = (R_earth * dlat_rad) * (
                R_earth * np.cos(np.deg2rad(lat)) * dlon_rad
            )

    return areacella


###############################
### REGRID A GIVEN VARIABLE ###
###############################


def regrid_field(
    dataset: xr.Dataset, field: str, output_grid: xr.Dataset
) -> xr.Dataset:
    """

    ---

    ### DEFINITION ###

    This function takes a xarray dataset as an input and regrids a given field on a provided output_grid.

    Why do we use regrid2 ?

    If performing conservative regridding from a high/medium resolution lat/lon grid to a coarse lat/lon target, Regrid2 may provide better results as it assumes grid cells with constant latitudes
    and longitudes while xESMF assumes the cells are connected by Great Circles (source : https://xcdat.readthedocs.io/en/latest/generated/xarray.Dataset.regridder.horizontal.html)

    ---

    ### INPUTS ###

    DATASET : XR DATASET | the dataset holding the field to be regridded

    FIELD : STR | the name of the field to be regridded

    OUTPUT_GRID : XR DATASET | the grid on which the regridding will be performed

    ---

    ### OUTPUTS ###

    FIELD_REGRIDDED : XR DATASET | the regridded field
    ---

    """

    field_regridded = dataset.regridder.horizontal(field, output_grid, tool="regrid2")

    return field_regridded


########################################
### ADD AREACELLA TO A GIVEN DATASET ###
########################################


def add_areacella_to_dataset(dataset: xr.Dataset, areacella: xr.Dataset) -> xr.Dataset:
    """

    ---

    ### DEFINITION ###

    This functions adds the areacella variable to a given dataset.

    ---

    ### INPUTS ###

    DATASET : XR DATASET | the dataset to which add areacella

    AREACELLA : XR DATASET | the areacella variable

    ---

    ### OUTPUTS ###

    DATASET : XR.DATASET | the dataset with areacella added in place
    ---

    """

    ### ADD AREACELLA TO THE DATASET ###

    dataset["areacella"] = (
        ("lat", "lon"),
        areacella,
    )

    return dataset


################################################################
### REGRID A LIST OF FIELDS AND GENERATE A REGRIDDED DATASET ###
################################################################


def regridding_a_dictionary(
    dictionary_to_be_regridded: dict[str, xr.Dataset],
    fields_to_be_regridded: list[str],
    output_grid: xr.Dataset,
) -> dict[str, xr.Dataset]:
    """

    ---

    ### DEFINITION ###

    This function takes as an input a 2D grid and generates the area for every grid cell. The result will be
    a map holding the area for every grid point.

    ---

    ### INPUTS ###

    GRID : XR DATASET | the dictionary holding the models' outputs

    ---

    ### OUTPUTS ###

    AREACELLA : NDArray[np.float64] | the areacella variable on the 2D grid given as an input
    ---

    """

    ### GET THE DICTIONARY KEYS ###

    keys_dict = list(dictionary_to_be_regridded.keys())

    ### INITIALIZE THE REGRIDDING WITH THE FIRST VARIABLE ###

    print("Initialize with one variable...\n")

    ## Extract the first field to initialize the new datasets ##

    field = fields_to_be_regridded[0]

    ## Initialize the new dictionary ##

    dict_regridded = {
        key: regrid_field(
            dataset=dictionary_to_be_regridded[key],
            field=field,
            output_grid=output_grid,
        )
        for key in keys_dict
    }

    ### REGRID THE REMAINING FIELDS ###

    ## Get the remaining fields to be regridded ##

    # Get the list #

    remaining_fields = fields_to_be_regridded[1:]

    # Get the number of remaining fields #

    n_fields = len(remaining_fields)

    ## Loop over the remaining fields ##

    for index in tqdm(range(n_fields), desc="Regridding all the variables..."):

        # Extract the field #

        field = remaining_fields[index]

        # Generate the dictionary of all models for one field #

        dict_regridded_given_field = {
            key: regrid_field(
                dataset=dictionary_to_be_regridded[key],
                field=field,
                output_grid=output_grid,
            )
            for key in keys_dict
        }

        # Add this one field to the full dictionnary #

        dict_regridded = {
            key: add_one_variable_to_dataset(
                variable_name=field,
                var_datarray=dict_regridded_given_field[key],
                modify_data=True,
                dataset=dict_regridded[key],
            )
            for key in keys_dict
        }

    ### ADD THE AREACELLA VARIABLE TO EVERY REGRIDDED DATASET ###

    ## Generate the areacella variable for the output grid ##

    output_areacella = compute_grid_areacella(output_grid)

    ## Add the areacella variable to every regridded dataset ##

    print("Adding areacella...\n")

    dict_regridded = {
        key: add_areacella_to_dataset(
            dataset=dict_regridded[key], areacella=output_areacella
        )
        for key in keys_dict
    }

    print("Done !")

    return dict_regridded
