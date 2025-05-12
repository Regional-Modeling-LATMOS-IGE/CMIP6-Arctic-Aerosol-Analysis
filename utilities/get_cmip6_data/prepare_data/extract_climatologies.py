#!/usr/bin/env python3

"""
This small script is used to treat the raw CMIP6 data we have downloaded. We transfom the single variable datasets that span over the 30-year simulation period
into monthly climatologies that are regrouped under the same model.variant hood.

We also build some tools to handle more easily the data structure.

Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""

##################################
### IMPORTATION OF THE MODULES ###
##################################

# ================ IMPORTATIONS ================ #

### DATA OBJECTS AND ASSOCIATED COMPUTATION ###

import numpy as np  # to handle numpy arrays and the associated tools

import xarray as xr  # to manage the data

import xcdat as xc  # to handle climate model outputs with xarray

### HOMEMADE LIBRARIES ###

from utilities.get_cmip6_data.load_raw_data.load_cmip6 import loading_cmip6  # function to load the raw data

from utilities.get_cmip6_data.store_data.dict_netcdf_transform import (
    dict_to_netcdf, # function to save the generated climatology
)  

#######################################################
### GENERATE DICTIONNARY KEYS WITHOUT THE VARIABLES ###
#######################################################


def generate_per_model_dict_key(dict_cmip6: dict):
    """
    ---

    ### DEFINITION ###

    This function receives the dictionnary keys from the raw loaded data dictionnary and change the variables with a *.
    It thens proceeds to make a unique key per model.variant couple and save them into a numpy array.

    ---

    ### INPUTS ###

    DICT_CMIP6 : DICT | dictionnary holding the raw loaded data

    ---

    ### OUTPUTS ###

    KEY_WITHOUT_VARIABLE_UNIQUE : NUMPY ARRAY OF STR | array with the one key per model with a * where the variables are written

    ---

    """

    ### RETRIEVE THE RAW LOADED DATA KEYS ###

    ## List of the keys ##

    list_keys = list(dict_cmip6.keys())

    ## Number of keys ##

    n_keys = len(list_keys)

    ## Generate the output array with the known number of keys ###

    keys_without_variable = np.empty(
        n_keys, dtype=object
    )  # dtype = object otherwise it truncates the str

    ### LOOP OVER THE DICTIONNARY KEYS ###

    for ii, key in enumerate(list_keys):

        ## Split the keys where there is a "." ##

        splitted_key = key.split(".")

        ## Copy the splitted key ##

        splitted_key_without_var = splitted_key

        ## Remove the variable and replace it with a * ##

        splitted_key_without_var[-1] = "*"

        ## Save it into the output numpy array ##

        keys_without_variable[ii] = splitted_key_without_var

    ### REMOVE THE DUPLICATES ###

    keys_without_variable_unique = np.unique(keys_without_variable)

    return keys_without_variable_unique


############################################
### ADD ONE VARIABLE TO A XARRAY DATASET ###
############################################


def add_one_variable_to_dataset(
    variable_name: str,
    var_datarray,
    modify_data: bool = False,
    dataset: bool = None,
    do_clim=False,
):
    """
    ### DEFINITION

    This function adds the variable_name variable to a xarray dataset with the var_datarray data array.
    If no datasets are provided, it will initialize them provided that modify_data is set to True.

    ### INPUTS

    VARIABLE_NAME : STR | variable to be added to the dataset

    VAR_DATARRAY : XARRAY DATA ARRAY | data array holding the variable variable_name to add to the xarray dataset

    MODIFY_DATA : BOOL | variable to say if we want to modify the input dataset

    DATASET : XARRAY DATASET | dataset without the new variable

    DO_CLIM : BOOL | bool defining if we compute the climatology or not by default set to True

    ### OUTPUTS

    DATASET : XARRAY DATASET | dataset with the new variable

    """

    ### PREPARE THE VARIABLE TO ADD ###

    ## Produce the climatology if needed ##

    if do_clim:

        var_to_add = var_datarray.temporal.climatology(
            variable_name, "month", weighted=True
        )  # we generate a monthly climatology

    ## Otherwise we just add the variable ##

    else:

        var_to_add = var_datarray

    ### ADDING THE VARIABLE TO THE DATASET ###

    ## Check wether we need to modify the dataset or not : if false initializes it / if true fills the provided ones ##

    if not modify_data:

        dataset = var_to_add

    else:

        dataset[variable_name] = (
            ("time", "lat", "lon"),
            var_to_add[variable_name].values,
        )

    ### DIFFERENT CORRECTIONS ###

    ## Test that the cloud fractions are expressed as fraction and modify it ##

    if variable_name == "clt":

        # If not a fraction turn it into a fraction #

        if np.max(dataset["clt"]) > 1.0:
            dataset["clt"] = dataset["clt"] / 100.0

    return dataset


##########################################
### CREATE THE CLIMATOLOGY DICTIONNARY ###
##########################################


def create_climatology_dict(
    data_path: str, data_folder_name: str, save_path: str, do_we_clear: bool = True
) -> dict:
    """
    ---

    ### DEFINITION

    This function generates the dictionnary of the xarray datasets holding every monthly climatology of the loaded raw variables.
    It then saves it as netcdf files for the provided save_path within the folder named save_folder_name.

    ---

    ### INPUTS

    DATA_PATH : STR | path of the parent directory of the raw data folder

    DATA_FOLDER_NAME : STR | name of the raw data folder

    SAVE_PATH : STR | path of the directory of the save folder

    DO_WE_CLEAR : BOOL | option to clear the save folder if it already exists : default is True

    ---

    ### OUTPUTS

    nothing.

    ---
    """

    ### INITIALIZATION ###

    ## Load the raw data ##

    dict_cmip6, dict_areacella = loading_cmip6(
        parent_path=data_path,
        downloading_folder_name=data_folder_name,
        do_we_clear=False,
    )

    print("Data dictionnary loaded\n")

    ## Create the dictionnary ##

    print("Generating the climatologies' dictionnary\n")

    dict_cmip6_clim = {}

    ## Generate the general key associated to each model.variant and experiment ##

    keys_without_variable_unique = generate_per_model_dict_key(dict_cmip6)

    ### GO THROUGH EACH MODEL.VARIANT AND EXPERIMENT ###

    for key in keys_without_variable_unique:

        ## Initialize the dataset with the first variable ##

        # Define the variable #

        var = variable_id[0]

        # Define that the dataset does not exist yet #

        modify_data = False

        # Copy the key without variable #

        key_with_var = key

        # Add the variable name #

        key_with_var[-2] = var

        # Generate the key by joining the str list with "." #

        key_with_var_full = ".".join(key_with_var)

        # Retrieve the variable data array #

        var_datarray = dict_cmip6[key_with_var_full]

        # Generate or update the dataset for the given model.variant and experiment #

        dataset_given_exp = add_one_variable_to_dataset(
            variable_name=var,
            var_datarray=var_datarray,
            modify_data=modify_data,
            do_clim=True,
        )

        # Set that now the dataset already exists #

        modify_data = True

        ## Go through the rest of the variables ##

        for var in variable_id[1:]:

            # Copy the key without variable #

            key_with_var = key

            # Add the variable name #

            key_with_var[-2] = var

            # Generate the key by joining the str list with "." #

            key_with_var_full = ".".join(key_with_var)

            # Retrieve the variable data array #

            var_datarray = dict_cmip6[key_with_var_full]

            # Update the dataset with the climatology of this variable #

            add_one_variable_to_dataset(
                variable_name=var,
                var_datarray=var_datarray,
                modify_data=modify_data,
                dataset=dataset_given_exp,
                do_clim=True,
            )

        ## Generate a new simpler key for dict_cmip6_clim ##

        # Retrieving the key information #

        source_id = key[2]

        experiment_id = key[3]

        member_id = key[4]

        grid_label = key[-1]

        # Create the new key #

        new_simpler_key_given_exp = ".".join([source_id, member_id, experiment_id])

        ## Use the gathered information to get the areacella entry of the given model.variant and experiment ##

        # Build the areacella key #

        key_areacella = ".".join([source_id, member_id, grid_label])

        # Retrieve the given areacella #

        areacella_datarray = dict_areacella[key_areacella]

        # Update the dataset of the given model.variant and experiment with the associated areacella #

        # test wether this works ?
        """
        dataset_given_exp["areacella"] = (
            ("lat", "lon"),
            areacella_datarray["areacella"].values,
        )
        """

        add_one_variable_to_dataset(
                variable_name="areacella",
                var_datarray=areacella_datarray,
                modify_data=modify_data,
                dataset=dataset_given_exp,
            )

        ## Add the dataset to the output dictionnary ##

        dict_cmip6_clim[new_simpler_key_given_exp] = dataset_given_exp

        ### SAVE THE GENERATED DICTIONNARY ###

        dict_to_netcdf(
            dataset_dict=dict_cmip6_clim, save_path=save_path, do_we_clear=True
        )

    print("Saving the climatologies' dictionnary\n")

    return


####################################################
### GENERATE THE ENTRIES WITHOUT THE EXPERIMENTS ###
####################################################


def get_model_entries__only_from_clim(key_with_exp: str) -> str:
    """
    ---
    ### DEFINITION ###

    This function receives a key from the climatology dictionnary and removes the experiment at the end to generate an only model and variants list.

    ---
    ### INPUTS ###

    KEY_WITH_EXP : STR | key of the climatology dictionnary holding the experiment specification at the end.

    ---
    ### OUTPUTS ###

    KEY_WITHOUT_EXP : STR | input key deprived of the experiment specification
    ---
    """

    ### REMOVE THE EXPERIMENT ###

    ## Split the key into a list of str ##

    splitted_key = key_with_exp.split(".")

    ## Remove the experiment specification at the end ##

    splitted_key_without_exp = splitted_key[:-1]

    ## Rejoin the newly formed key ##

    key_without_exp = ".".join(splitted_key_without_exp)

    return key_without_exp


######################
### USED FOR TESTS ###
######################

if __name__ == "__main__":

    pass
