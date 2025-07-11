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

### DATA OBJECTS AND ASSOCIATED COMPUTATION ###

import numpy as np  # to handle numpy arrays and the associated tools

import xarray as xr  # to manage the data

import xcdat as xc  # to handle climate model outputs with xarray

### PROGRESS BAR ###

from tqdm import tqdm

### TYPE HINTS FOR FUNCTIONS ###

from numpy.typing import NDArray

### HOMEMADE LIBRARIES ###

from utilities.get_cmip6_data.load_raw_data.load_cmip6 import (
    loading_cmip6,  # to load the raw data and areacella
    set_search_criterias,  # to access the chosen search criteria
)  # function to load the raw data

from utilities.get_cmip6_data.store_data.dict_netcdf_transform import (
    dict_to_netcdf,  # function to save the generated climatology
)

#######################################################
### GENERATE DICTIONARY KEYS WITHOUT THE VARIABLES ####
#######################################################


def generate_per_model_dict_key(full_cmip6_dict: dict) -> NDArray[object]:
    """

    ---

    ### DEFINITION ###

    This function receives the dictionary keys from the raw loaded data dictionary and change the variables with a *.
    It thens proceeds to make a unique key per model.variant couple and save them into a numpy array.

    ---

    ### INPUTS ###

    full_cmip6_dict : DICT | dictionary holding the raw loaded data

    ---

    ### OUTPUTS ###

    KEY_WITHOUT_VARIABLE_UNIQUE : NUMPY ARRAY OF STR | array with the one key per model with a * where the variables are written

    ---

    """

    ### RETRIEVE THE RAW LOADED DATA KEYS ###

    ## List of the keys ##

    list_keys = list(full_cmip6_dict.keys())

    ## Number of keys ##

    n_keys = len(list_keys)

    ## Generate the output array with the known number of keys ###

    keys_without_variable = np.empty(
        n_keys, dtype=object
    )  # dtype = object otherwise it truncates the str

    ### LOOP OVER THE dictionary KEYS ###

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
    var_datarray: xr.DataArray,
    modify_data: bool = False,
    dataset: xr.Dataset = None,
    do_clim=False,
) -> xr.Dataset:
    """
    ---

    ### DEFINITION

    This function adds the variable_name variable to a xarray dataset with the var_datarray data array.
    If no datasets are provided, it will initialize them provided that modify_data is set to True.

    ---

    ### INPUTS

    VARIABLE_NAME : STR | variable to be added to the dataset

    VAR_DATARRAY : XARRAY DATA ARRAY | data array holding the variable variable_name to add to the xarray dataset

    MODIFY_DATA : BOOL | variable to say if we want to modify the input dataset

    DATASET : XARRAY DATASET | dataset without the new variable

    DO_CLIM : BOOL | bool defining if we compute the climatology or not by default set to False

    ---

    ### OUTPUTS

    DATASET : XARRAY DATASET | dataset with the new variable

    ---
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
            var_datarray[variable_name].values,
        )

    ### DIFFERENT CORRECTIONS ###

    ## Test that the cloud fractions are expressed as fraction and modify it ##

    if variable_name == "clt":

        # If not a fraction turn it into a fraction #

        if (
            np.mean(dataset["clt"]) > 1.0
        ):  # mean to consider the whole variable and not odd points
            dataset["clt"] = dataset["clt"] / 100.0

    return dataset


##########################################
### CREATE THE CLIMATOLOGY DICTIONARY ###
##########################################


def create_climatology_dict(
    data_path: str,
    data_folder_name: str,
    parent_path_for_save: str,
    selected_case: str,
    remove_ensembles: bool = False,
    do_we_clear: bool = False,
    verbose: bool = False,
):
    """
    ---

    ### DEFINITION

    This function generates the dictionary of the xarray datasets holding every monthly climatology of the loaded raw variables.
    It then saves it as netcdf files for the provided save_path within the folder named save_folder_name.

    ---

    ### INPUTS

    DATA_PATH : STR | path of the parent directory of the raw data folder

    DATA_FOLDER_NAME : STR | name of the raw data folder

    PARENT_PATH_FOR_SAVE : STR | path of the directory of the save folder

    SELECTED_CASE : STR | case selected for the loading of the raw data

    REMOVE_ENSEMBLE : BOOL | option to keep only one variant per model

    DO_WE_CLEAR : BOOL | option to clear the save folder if it already exists : default is True

    VERBOSE : BOOL | option to keep the warnings regarding connection failures to esgf servers

    ---

    ### OUTPUTS

    nothing.

    ---
    """

    ### INITIALIZATION ###

    ## Load the raw data ##

    full_cmip6_dict, dict_areacella = loading_cmip6(
        parent_path=data_path,
        downloading_folder_name=data_folder_name,
        case=selected_case,
        remove_ensembles=remove_ensembles,
        do_we_clear=do_we_clear,
        verbose=verbose,
    )

    print("Data dictionary loaded\n")

    ## Retrieve the given search criterias to know the variables we have loaded ##

    search_criterias = set_search_criterias(
        case=selected_case,
    )  # it's a dictionary with all the needed global search criterias to set

    # Get the search facets #

    search_facets = search_criterias["search_facets"]

    # Get the variables we are looking for #

    variable_id = search_facets["variable_id"]

    ## Create the dictionary ##

    full_cmip6_dict_clim = {}

    ## Generate the general key associated to each model.variant and experiment ##

    keys_without_variable_unique = generate_per_model_dict_key(full_cmip6_dict)

    ## Define the number of unique entry and experiments couples ##

    n_entry_and_exp = len(keys_without_variable_unique)

    ### GO THROUGH EACH MODEL.VARIANT.GRID AND EXPERIMENT ###

    ## Define a progress bar while we go through the unique entry keys ##

    for index in tqdm(
        range(n_entry_and_exp), desc="Generating the climatologies' dictionnary..."
    ):

        ## Retrieve the key ##

        key = keys_without_variable_unique[index]

        ## Initialize the dataset with the first variable ##

        # Define the variable #

        var = variable_id[0]

        # Define that the dataset does not exist yet #

        modify_data = False

        # Copy the key without variable #

        key_with_var = key

        # Add the variable name #

        key_with_var[-1] = var

        # Generate the key by joining the str list with "." #

        key_with_var_full = ".".join(key_with_var)

        # Retrieve the variable data array #

        var_datarray = full_cmip6_dict[key_with_var_full]

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

            key_with_var[-1] = var

            # Generate the key by joining the str list with "." #

            key_with_var_full = ".".join(key_with_var)

            # Retrieve the variable data array #

            var_datarray = full_cmip6_dict[key_with_var_full]

            # Update the dataset with the climatology of this variable #

            add_one_variable_to_dataset(
                variable_name=var,
                var_datarray=var_datarray,
                modify_data=modify_data,
                dataset=dataset_given_exp,
                do_clim=True,
            )

        ## Generate the key for full_cmip6_dict_clim ##

        # Retrieving the key information #

        # key =  [source_id, member_id, grid, experiment_id, '*']

        source_id = key[0]

        member_id = key[1]

        grid_label = key[2]

        experiment_id = key[3]

        # Create the new key #

        new_simpler_key_given_exp = ".".join(
            [source_id, member_id, grid_label, experiment_id]
        )

        ## Use the gathered information to get the areacella entry of the given model.variant and experiment ##

        # Build the areacella key #

        key_areacella = ".".join([source_id, member_id, grid_label])

        # Retrieve the given areacella #

        areacella_datarray = dict_areacella[key_areacella]

        # Update the dataset of the given model.variant and experiment with the associated areacella #

        dataset_given_exp["areacella"] = (
            ("lat", "lon"),
            areacella_datarray["areacella"].values,
        )

        ## Add the dataset to the output dictionnary ##

        full_cmip6_dict_clim[new_simpler_key_given_exp] = dataset_given_exp

    ### SAVE THE GENERATED DICTIONARY ###

    print("\nSaving the climatologies' dictionary...\n")

    dict_to_netcdf(
        dataset_dict=full_cmip6_dict_clim,
        parent_path_for_save=parent_path_for_save,
        do_we_clear=do_we_clear,
    )
    return


######################
### USED FOR TESTS ###
######################

if __name__ == "__main__":

    pass
