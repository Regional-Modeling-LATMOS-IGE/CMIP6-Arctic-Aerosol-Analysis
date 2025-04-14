#!/usr/bin/env python3

"""
This small script is used to treat the raw CMIP6 data we have downloaded. We transfom the single variable datasets that span over the 30-year simulation period
into monthly climatologies that are regrouped under the same model.variant hood.

Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""

##################################
### IMPORTATION OF THE MODULES ###
##################################

# ================ IMPORTATIONS ================ #

### LOAD AND NAVIGATE THROUGH THE DATA ###

import os  # to get access to commands related to path setting and creation of directories

import intake_esgf  # this gives us access to the ESGF catalog to make queries

### DATA OBJECTS AND ASSOCIATED COMPUTATION ###

import numpy as np  # to handle numpy arrays and the associated tools

import xarray as xr  # to manage the data

import xcdat as xc  # to handle climate model outputs with xarray

import pandas as pd  # to create and handle tables in python

### HOMEMADE LIBRARIES ###

from utilities.download.load_cmip6 import loading_cmip6 # function to load the raw data

from utilities.download.folders_handle.create import create_dir  # function to create a cleaned downloading directory

#######################
#### INITIALISATION ###
#######################

# ================ DEFINE THE FOLDERS WHERE IS STORED THE DATA ================ #

### DEFINE THE HOME DIRECTORY ###

## Home directory ##

homedir_path = os.path.expanduser("~")

### DEFINE WHERE IS THE DOWNLOADED RAW DATA ###

## Parent directory ##

parent_path_download = homedir_path + "/certainty-data"

## Name of the created folder ##

download_folder_name = "CMIP6-DATA"

### DEFINE WHERE TO SAVE THE CLIMATOLOGIES ###

## Parent directory ##

parent_path_save = homedir_path + "/certainty-data/CMIP6-DATA/"

## Name of the created folder ##

saving_folder_name = "treated-data"

# ================ SEARCH CRITERIAS FOR OUR ANALYSIS ================ #

### VARIABLES ###

variable_id = [
    "clt",
    "rsdt",
    "rsut",
    "rsutcs",
    "rsds",
    "rsus",
    "rsdscs",
    "rsuscs",
    "rlut",
    "rlutcs",
    "rlds",
    "rlus",
]

#######################################################
### GENERATE DICTIONNARY KEYS WITHOUT THE VARIABLES ###
#######################################################


def generate_per_model_dict_key(dict_cmip6 : dict):

    """

    ### DEFINITION ###

    This function receives the dictionnary keys from the raw loaded data dictionnary and change the variables with a *.
    It thens proceeds to make a unique key per model.variant couple and save them into a numpy array.

    ### INPUTS ###

    DICT_CMIP6 : DICT | dictionnary holding the raw loaded data

    ### OUTPUTS ###

    KEY_WITHOUT_VARIABLE_UNIQUE : NUMPY ARRAY OF STR | array with the one key per model with a * where the variables are written

    """

    ### RETRIEVE THE RAW LOADED DATA KEYS ###

    ## List of the keys ##

    list_keys = list(dict_cmip6.keys())

    ## Number of keys ##

    n_keys = len(list_keys)

    ## Generate the output array with the known number of keys ###

    keys_without_variable = np.empty(n_keys, dtype=object)  # dtype = object otherwise it truncates the str

    ### LOOP OVER THE DICTIONNARY KEYS ###

    for ii, key in enumerate(list_keys):

        ## Split the keys where there is a "." ##

        splitted_key = key.split(".")

        ## Copy the splitted key ##

        splitted_key_without_var = splitted_key

        ## Remove the variable and replace it with a * ##

        splitted_key_without_var[-2] = "*"

        ## Save it into the output numpy array ##

        keys_without_variable[ii] = splitted_key_without_var

    ### REMOVE THE DUPLICATES ###

    keys_without_variable_unique = np.unique(keys_without_variable)

    return keys_without_variable_unique

############################################
### ADD ONE VARIABLE TO A XARRAY DATASET ###
############################################

def add_one_variable_to_dataset(variable_name: str, var_datarray, modify_data:bool=False, dataset:bool=None):

    """
    ### DEFINITION

    This function adds the variable_name variable to a xarray dataset with the var_datarray data array. 
    If no datasets are provided, it will initialize them provided that modify_data is set to True.

    ### INPUTS

    VARIABLE_NAME : STR | variable to be added to the dataset

    VAR_DATARRAY : XARRAY DATA ARRAY | data array holding the variable variable_name to add to the xarray dataset

    MODIFY_DATA : BOOL | variable to say if we want to modify the input dataset

    DATASET : XARRAY DATASET | dataset without the new variable

    ### OUPUTS

    DATASET : XARRAY DATASET | dataset with the new variable 

    """

    ### MAKE CLIMATOLOGIES ###

    ## Produce the climatology ##

    var_climatology = var_datarray.temporal.climatology(
        variable_name, "month", weighted=True
    )  # we generate a monthly climatology


    ### ADDING THE VARIABLE TO THE DATASET ###

    ## Check wether we need to modify the dataset or not : if false initializes it / if true fills the provided ones ##

    if not modify_data:

        dataset = var_climatology

    else:

        dataset[variable_name] = (
            ("time", "lat", "lon"),
            var_climatology[variable_name].values,
        )

    ### DIFFERENT CORRECTIONS ###

    ## Test that the cloud fractions are expressed as fraction and modify it ##

    if variable_name == "clt":

        # If not a fraction turn it into a fraction #

        if np.max(dataset["clt"]) > 1.0:
            dataset["clt"] = dataset["clt"] / 100.0

    return dataset