#!/usr/bin/env python3

"""
This small script is used to treat the save and load the data we have prepared for analysis. 
We transform a dictionnary structure into a series of netcdf files for every single model, variant and experiment.
We are able to reload the same structure from the netcdf files. To do so, we generate a dataframe associating each entry to its path and save it 
as a pickle file.

Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""

##################################
### IMPORTATION OF THE MODULES ###
##################################

### DATA OBJECTS AND ASSOCIATED COMPUTATION ###

import numpy as np  # to handle numpy arrays and the associated tools

import xarray as xr  # to manage the data

import pandas as pd # to create and handle tables in python

### HOMEMADE LIBRARIES ###

from utilities.download.folders_handle.create import (
    create_dir,
)  # function to create a cleaned downloading directory

#############################################################
### SAVE EVERY DATASET OF THE DICTIONNARY AS NETCDF FILES ###
#############################################################

def dict_to_netcdf(dataset_dict : dict, save_path : str, save_folder_name : str, do_we_clear:bool = True):
    
    """
    ### DEFINITION ###

    This function save every dataset entry of the dictionnary and save them as netcdf files. It also generates a pandas dataframe associating every single key 
    of the dictionnary with the path of the corresponding saved netcdf file. This dataframe is saved as a pickle file.

    ### INPUTS ###

    DATASET_DICT : DICTIONNARY OF XARRAY DATASETS | dictionnary of the datasets we want to save 

    SAVE_PATH : STR | path of the parent directory of the save folder

    SAVE_FOLDER_NAME : STR | name to be given to the save folder

    DO_WE_CLEAR : BOOL | option to clear the save folder if it already exists : default is True

    ### OUTPUTS ###

    nothing.
    """
    
    ### INITIALISATION ###

    ## Get the list of the keys of the dictionnary #

    # Extract the list #

    list_keys = list(dataset_dict.keys())

    # Get the number of keys #

    n_keys = len(list_keys)

    ## Generate the array of the paths ##

    paths = np.empty(n_keys, dtype=object)  # dtype = object otherwise it truncates the str

    ### GO THROUGH THE ENTRIES ###

    for ii, key in enumerate(list_keys):

        ## Generate a filename with the key ##

        # Split the key into a list of keywords #

        splitted_key = key.split(".")

        # Connect them with a "_" to make a filename that is not broken #

        full_name = "_".join(splitted_key)

        # Define the filename #

        filename = full_name + ".nc"

        ## Create the directory associated to the entry and keep its path ##

        saving_path_given_entry = create_dir(
            parent_path= save_path, name=full_name, clear=do_we_clear
        )

        ## Generate the full path with the filename ##

        path_to_nc = saving_path_given_entry + "/" + filename

        ## Save the entry's dataset ##

        # Save it #

        dataset_dict[key].to_netcdf(path=path_to_nc)

        # Conserve the path at which we saved it in the array #

        paths[ii] = path_to_nc

    ### GENERATE THE PANDAS DATAFRAME ASSOCIATING KEYS WITH PATHS ###

    ## Create the pandas dataframe from a dictionnary ##

    # Define the table key vs path #

    key_paths_dict = {"key": list_keys, "path": paths}

    # Define the dataframe #

    key_paths_table = pd.DataFrame(key_paths_dict)

    # Save it as a pickle file #

    key_paths_table.to_pickle(save_path + "/" + "key_paths_table.pkl")

    return 


####################################################
### GENERATE A DICTIONNARY FROM THE NETCDF FILES ###
####################################################


def netcdf_to_dict(save_path : str):
    
    """
    ### DEFINITION ###

    This function loads every entry identified in a pandas dataframe at the input path.
    It then loads them into a dictionnary with the keys provided by the dataframe.

    ### INPUTS ###

    SAVE_PATH : STR | path of the directory where the data was saved

    ### OUTPUTS ###

    GENERATED_DATA_DICT : DICT | dictionnary holding the datasets saved at save_path
    """

    ### INITIALISE ###

    ## Generate the output dictionnary ##

    generated_data_dict = {}

    ## Retrieve the paths and keys from the dataframe located at save_path ##

    # Load the dataframe #

    key_paths_table = pd.read_pickle(save_path + "/" + "key_paths_table.pkl")

    # Extract the keys #

    list_keys = key_paths_table["key"].to_list()
    
    # Extract the associated paths #

    paths = key_paths_table["path"].to_list()

    ### REBUILD THE SAVED DICTIONNARY ###

    for ii, key in enumerate(list_keys):

        ## Retrieve the path ##

        path_to_nc = paths[ii]

        ## Load the netcdf file into the dictionnary #

        generated_data_dict[key] = xr.open_dataset(path_to_nc)
    
    return generated_data_dict
