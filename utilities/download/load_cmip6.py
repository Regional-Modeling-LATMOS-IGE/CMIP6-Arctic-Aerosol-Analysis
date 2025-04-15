#!/usr/bin/env python3

"""
This small script is used to load the CMIP6 data used for the analysis.
For more details on the methods employed in the script, please refer to the download_cmip6.ipynb notebook in the same folder.

!!! THE SEARCH CRITERIAS ARE DEFINED GLOBALLY  WITHIN THIS SCRIPT AS THEY ARE NOT EXPECTED TO CHANGE FOR THE ANALYSIS !!!

Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""

##################################
### IMPORTATION OF THE MODULES ###
##################################

# ================ IMPORTATIONS ================ #

### LOAD AND NAVIGATE THROUGH THE DATA ###

import intake_esgf  # this gives us access to the ESGF catalog to make queries

### DATA OBJECTS AND ASSOCIATED COMPUTATION ###

import numpy as np  # to manage the pandas arrays

### HOMEMADE LIBRARIES ###

from utilities.download.folders_handle.create import (
    create_dir,
)  # function to create a cleaned downloading directory

#######################
#### INITIALISATION ###
#######################

# ================ SEARCH CRITERIAS FOR OUR ANALYSIS ================ #

### EXPERIMENTS ###

experiment_id = [
    "piClim-control",
    "piClim-aer",
]

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

### TABLE ###

table_id = "Amon"

### SET THE EXPECTED NUMBER OF FILES : number_of_experiments * number_of_variables ###

expected_number_of_files = np.size(experiment_id) * np.size(variable_id)

###################################
#### SET THE DOWNLOADING FOLDER ###
###################################


def set_downloading_folder(
    parent_path: str, downloading_folder_name: str, do_we_clear: bool = False
):
    """
    ### DEFINITION ###

    This function prepares the downloading folder and sets it. It will create or check if a download folder exists at
    the path download_folder_path. It will erase a pre-existing folder if the do_we_clear option is set to True.
    This can be quite slow if the data folder is already holding some heavy data. Then, it will configure the intake-esgf catalog
    to look there for the data.

    ### INPUTS ###

    PARENT_PATH : STR | path of the parent directory of the download folder

    DOWNLOADING_FOLDER_NAME : STR | name to be given to the download folder

    DO_WE_CLEAR : BOOL | option to clear the downloading folder if it already exists

    ### OUTPUTS ###

    nothing.
    """

    ### CREATE THE DIRECTORY AND EMPTY IF MAKE_A_NEW_FOLDER ###

    downloading_path = create_dir(
        parent_path=parent_path, name=downloading_folder_name, clear=do_we_clear
    )

    ### SET THE DOWNLOADING PATH ###

    intake_esgf.conf.set(local_cache=downloading_path)

    print(
        "The CMIP6 data will be searched at the path : {}\n".format(
            intake_esgf.conf["local_cache"]
        )
    )

    return


#######################################################
#### FILTERING FUNCTION DEFINING INCOMPLETE ENTRIES ###
#######################################################


def filtering_function(model_group) -> bool:
    """

    ### DEFINITION ###

    This function allows the intake-esgf catalog to be cleaned of the entries that are not complete.
    In this case it means entries that do not meet the expected number of files

    """

    if len(model_group) == expected_number_of_files:

        return True


##########################################
#### GETTING THE AREACELLA DICTIONNARY ###
##########################################


def get_areacella_apart(catalog) -> dict:
    """

    ### DEFINITION ###

    This function loads an areacella dictionnary for every single entry of the catalog.

    ### INPUTS ###

    CATALOG : intake-esgf object | the catalog we defined with our search criterias

    ### OUTPUTS ###

    DICT_AREACELLA : dictionnary | hold an areacella xarray data array for every entry in the catalog

    """

    ### INITIALISATION  ###

    ## Initialise the full dictionnary ##

    dict_areacella = {}

    ## Models grouped by SOURCE_ID | MEMBER_ID | GRID_LABEL ##

    series_grouped_models = catalog.model_groups()

    ## Number of rows ##

    n_rows = series_grouped_models.size

    ### GO THROUGH EVERY ROW OF THE PANDA SERIES ###

    for ii in range(n_rows):

        ## Get the SOURCE_ID | MEMBER_ID | GRID_LABEL of the row ##

        # Retrieve the row ##

        row_ii = series_grouped_models.index[ii]

        # Extract the labels #

        source_id, member_id, grid_label = row_ii

        # Build the key for this dictionnary entry ##

        full_key = source_id + "." + member_id + "." + grid_label

        ## Special case for the IPSL-CM6A-LR-INCA model ##

        if source_id == "IPSL-CM6A-LR-INCA":

            source_id = "IPSL-CM6A-LR"

        ## Do the full search ##

        areacella_search_full = catalog.search(
            source_id=source_id,
            grid_label=grid_label,
            variable_id="areacella",
            quiet=True,
        ).df  # silence the progress bar

        ## Extract the first experiment id that gives an areacella entry ##

        only_first_exp_id = areacella_search_full.experiment_id.values[0]

        ## Extract the first member id that gives an areacella entry ##

        only_first_member_id = areacella_search_full.member_id.values[0]

        ## Get the areacella for the given row ##

        # Search and download it #

        areacella_ii = catalog.search(
            source_id=source_id,
            grid_label=grid_label,
            variable_id="areacella",
            experiment_id=only_first_exp_id,
            member_id=only_first_member_id,
            quiet=True,
        ).to_dataset_dict(
            add_measures=False, quiet=True
        )  # silence the progress bar

        # Store it in dictionnary #

        dict_areacella[full_key] = areacella_ii["areacella"]

    return dict_areacella


###########################
#### LOADING CMIP6 DATA ###
###########################


def loading_cmip6(
    parent_path: str, downloading_folder_name: str, do_we_clear: bool = False
) -> dict:
    """

    ### DEFINITION ###

    This function loads the CMIP6 data ensemble under the form of a dictionnary structure.

    ### INPUTS ###

    PARENT_PATH : STR | path of the parent directory of the download folder

    DOWNLOADING_FOLDER_NAME : STR | name to be given to the download folder

    DO_WE_CLEAR : BOOL | option to clear the downloading folder if it already exists

    ### OUTPUTS ###

    DICT_CMIP6 : dictionnary | hold a xarray data array for every variable of every single entry in the catalog

    SEARCH_DATAFRAME : pandas dataframe | hold all the information about the found entries

    DICT_AREACELLA : dictionnary | hold an areacella xarray data array for every entry in the catalog
    """

    ### SET THE DOWNLOADING FOLDER ###

    set_downloading_folder(
        parent_path=parent_path,
        downloading_folder_name=downloading_folder_name,
        do_we_clear=do_we_clear,
    )

    ### INITIALIZE THE CATALOG ###

    catalog = intake_esgf.ESGFCatalog()

    print(
        "The search criterias are : {}\n{}\n{}\n".format(
            experiment_id, variable_id, table_id
        )
    )

    ### SET THE SEARCH CRITERIAS (defined globally in this script) ###

    print("Filling the catalog with the search criterias...\n")

    catalog.search(
        experiment_id=experiment_id,
        variable_id=variable_id,
        table_id=table_id,
        quiet=True,
    )

    ### REMOVE THE INCOMPLETE ENTRIES ###

    catalog = catalog.remove_incomplete(filtering_function)

    ### REMOVE THE VARIANT DUPLICATES ###

    catalog = catalog.remove_ensembles()

    ### LOAD THE DICTIONNARY INTO MEMORY WITHOUT AREACELLA ###

    print("Downloading and/or loading the data dictionnary\n")

    dict_cmip6 = catalog.to_dataset_dict(
        add_measures=False,
        ignore_facets=["activtity_drs", "institution_id, table_id"],
        quiet=True,
    )

    ### LOAD THE AREACELLA DICTIONNARY APART THANKS TO THE CATALOG ###

    print("Downloading and/or loading the areacella dictionnary\n")

    dict_areacella = get_areacella_apart(catalog)

    return dict_cmip6, dict_areacella


######################
### USED FOR TESTS ###
######################

if __name__ == "__main__":

    pass
