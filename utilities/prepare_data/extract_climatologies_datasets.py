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


def generate_per_model_dict_key(dict_cmip6 : dict):
    
    list_keys = list(dict_cmip6.keys())

    n_keys = len(list_keys)

    keys_without_variable = np.empty(n_keys, dtype=object)  # otherwise it truncates the str


    for ii, key in enumerate(list_keys):

        splitted_key = key.split(".")

        # copy the splitted key

        splitted_key_without_var = splitted_key

        # remove the variable

        splitted_key_without_var[-2] = "*"

        keys_without_variable[ii] = splitted_key_without_var

    # remove the duplicates (not the more efficient way of doing it but simpler)

    keys_without_variable_unique = np.unique(keys_without_variable)

    return