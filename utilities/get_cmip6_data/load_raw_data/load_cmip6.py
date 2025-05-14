#!/usr/bin/env python3

"""
This submodule is used to load the raw CMIP6 data used for the analysis.
For more details on the methods employed in the script, please refer to the get_cmip6_data.ipynb notebook in the same folder.

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

import pandas as pd  # to manage the product of the search

### WARNINGS HANDLING ###

import warnings

### HOMEMADE LIBRARIES ###

from utilities.get_cmip6_data.folders_handle.create import (
    create_dir,  # function to create a cleaned downloading directory
)

#############################
#### DEFINE CUSTOM ERRORS ###
#############################


class InvalidCase(Exception):

    ### DEFINING THE EXCEPTION PROPERTIES ###

    def __init__(
        self, case, error_msg="The following case is not covered for the search"
    ):
        self.case = case
        self.error_msg = error_msg
        super().__init__(self.msg)  # calling the exception parent class

    ### DEFINING THE ERROR MESSAGE ###

    def __str__(self):  # what happens when printing the error
        return f"{self.case} -> {self.error_msg}"


#############################################
#### DEFINE GLOBALLY THE SEARCH CRITERIAS ###
#############################################


def set_search_criterias(case: str) -> dict:
    """

    ---

    ### DEFINITION ###

    This function allows us to define dynamically the search criterias in function of the case we are in.

    ---

    ### INPUTS ###

    CASE : STR | str defining the case for the search :

        - SW (short-wave variables for the APRP method)
        - ZELINKA-SW (short-wave variables for the APRP method by keeping only the models and variants present in Zelinka and al. (2023))

    ---

    ### OUTPUTS ###

    SEARCH : DICT | dictionary holding the search criterias

    EXPECTED_NUMBER_OF_FILES : INT | expected number of files such that on model_id and source_id couples corresponds to (number_of_variables) * (number_of_experiments)

    ---

    ### REFERENCES ###

    Zelinka, M. D., Smith, C. J., Qin, Y., and Taylor, K. E.: Comparison of methods to estimate aerosol effective radiative forcings in climate models,
    Atmos. Chem. Phys., 23, 8879–8898, https://doi.org/10.5194/acp-23-8879-2023, 2023.

    ---
    """

    ### SHORT-WAVE ONLY CASE ###

    if case == "SW":

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
        ]

        ### TABLE ###

        table_id = "Amon"

        ### DEFINE SEARCH CRITERIAS DICTIONARY ###

        search_facets = {
            "experiment_id": experiment_id,
            "variable_id": variable_id,
            "table_id": table_id,
        }

        # ================ EXPECTED NUMBER OF FILES ================ #

        expected_number_of_files = 16  # 8 variables * 2 experiments

        return {
            "search_facets": search_facets,
            "expected_number_of_files": expected_number_of_files,
            "filtering_by_name": False,
            "keep_only_dataframe": None,
        }

    elif case == "ZELINKA-SW":

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
        ]

        ### TABLE ###

        table_id = "Amon"

        ### DEFINE SEARCH CRITERIAS DICTIONARY ###

        search_facets = {
            "experiment_id": experiment_id,
            "variable_id": variable_id,
            "table_id": table_id,
        }

        # ================ EXPECTED NUMBER OF FILES ================ #

        expected_number_of_files = 16  # 8 variables * 2 experiments

        # ================ DEFINE THE MODEL.VARIANT LIST OF ZELINKA'S ARTICLE ================ #

        source_id_zelinka_2023 = [
            "ACCESS-CM2",
            "ACCESS-ESM1-5",
            "BCC-ESM1",
            "CESM2",
            "CNRM-CM6-1",
            "CNRM-ESM2-1",
            "CanESM5",
            "GFDL-CM4",
            "GFDL-ESM4",
            "GISS-E2-1-G",
            "GISS-E2-1-G",
            "GISS-E2-1-G",
            "HadGEM3-GC31-LL",
            "IPSL-CM6A-LR-INCA",
            "IPSL-CM6A-LR",
            "IPSL-CM6A-LR",
            "IPSL-CM6A-LR",
            "IPSL-CM6A-LR",
            "MIROC6",
            "MIROC6",
            "MPI-ESM-1-2-HAM",
            "MRI-ESM2-0",
            "NorESM2-LM",
            "NorESM2-LM",
            "NorESM2-MM",
            "UKESM1-0-LL",
        ]

        member_id_zelinka_2023 = [
            "r1i1p1f1",
            "r1i1p1f1",
            "r1i1p1f1",
            "r1i1p1f1",
            "r1i1p1f2",
            "r1i1p1f2",
            "r1i1p2f1",
            "r1i1p1f1",
            "r1i1p1f1",
            "r1i1p1f1",
            "r1i1p1f2",
            "r1i1p3f1",
            "r1i1p1f3",
            "r1i1p1f1",
            "r1i1p1f1",
            "r2i1p1f1",
            "r3i1p1f1",
            "r4i1p1f1",
            "r11i1p1f1",
            "r1i1p1f1",
            "r1i1p1f1",
            "r1i1p1f1",
            "r1i1p1f1",
            "r1i1p2f1",
            "r1i1p1f1",
            "r1i1p1f4",
        ]

        zelinka_2023_model_variant_table = pd.DataFrame(
            {"source_id": source_id_zelinka_2023, "member_id": member_id_zelinka_2023},
            dtype=str,
        )

        return {
            "search_facets": search_facets,
            "expected_number_of_files": expected_number_of_files,
            "filtering_by_name": True,
            "keep_only_dataframe": zelinka_2023_model_variant_table,
        }

    ### THE INPUT CASE IS NOT COVERED ###

    else:

        raise InvalidCase


###################################
#### SET THE DOWNLOADING FOLDER ###
###################################


def set_downloading_folder(
    parent_path: str, downloading_folder_name: str, do_we_clear: bool = False
):
    """
    ---

    ### DEFINITION ###

    This function prepares the downloading folder and sets it. It will create or check if a download folder exists at
    the path download_folder_path. It will erase a pre-existing folder if the do_we_clear option is set to True.
    This can be quite slow if the data folder is already holding some heavy data. Then, it will configure the intake-esgf catalog
    to look there for the data.

    ---

    ### INPUTS ###

    PARENT_PATH : STR | path of the parent directory of the download folder

    DOWNLOADING_FOLDER_NAME : STR | name to be given to the download folder

    DO_WE_CLEAR : BOOL | option to clear the downloading folder if it already exists

    ---

    ### OUTPUTS ###

    nothing.

    ---
    """

    ### CREATE THE DIRECTORY AND EMPTY IF MAKE_A_NEW_FOLDER ###

    downloading_path = create_dir(
        parent_path=parent_path, name=downloading_folder_name, clear=do_we_clear
    )

    ### SET THE DOWNLOADING PATH ###

    intake_esgf.conf.set(local_cache=downloading_path)

    print(
        "The CMIP6 data will be searched and downloaded at the path : {}\n".format(
            intake_esgf.conf["local_cache"]
        )
    )

    return


########################################################################################
#### FILTERING FUNCTION REMOVING INCOMPLETE ENTRIES AND KEEPING ONLY PROVIDED MODELS ###
########################################################################################


# ================ DEFINE THE FILTERING FUNCTION ================ #


def filtering_function(grouped_model_entry: pd.DataFrame) -> bool:
    """
    ---

    ### DEFINITION ###

    This function allows the intake-esgf catalog to be cleaned of the entries that are not complete.
    In the default case it means entries that do not meet the expected number of files.

    The user can also set a condition that only the model and variant couples present in a provided pandas dataframe are kept.
    Since the nature of this function is to be an input for the intake-esgf package, we define the optional arguments outside
    of the function.

    ---

    ### INPUTS

    GROUPED_MODEL_ENTRY : Pandas DataFrame | sub dataframe containing all the variables of a given source_id, member_id and grid tuple.

    ---

    ### OPTIONAL ARGUMENTS (DEFINED GLOBALLY)

    FILTERING_BY_NAME : BOOL | defines if we filter the entry by source_id and member_id or not

    KEEP_ONLY_DATAFRAME : Pandas DataFrame | associated dataframe holding the source_id and member_id to conserve

    ---

    ### OUTPUTS

    OUTPUT : BOOL | whether we keep this model group or not

    ---
    """

    ### INITIALISATION ###

    ### TEST THE NUMBER OF VARIBALES ###

    if len(grouped_model_entry) == expected_number_of_files:

        ### NUMBER OF VARIABLES' TEST SUCCEEDED ###

        ## Do we keep only the keep_only_dataframe model and variant couples ? ##

        # NO : We keep everything that matched the variable number's test #

        if not (filtering_by_name):

            return True

        ### YES : KEEPING ONLY THE COUPLES PRESENT IN KEEP_ONLY_DATAFRAME ###

        else:

            ## Doing the test on the grouped_model_entry's source_id and member_id ##

            # Extract the grouped_model_entry data #

            grouped_model_entry_source_id = grouped_model_entry.source_id.unique()[0]

            grouped_model_entry_member_id = grouped_model_entry.member_id.unique()[0]

            # Can we find the grouped_model_entry's source_id and member_id in one row of is_in_keep_only_dataframe ? #

            is_in_keep_only_dataframe = (
                (keep_only_dataframe["source_id"] == grouped_model_entry_source_id)
                & (keep_only_dataframe["member_id"] == grouped_model_entry_member_id)
            ).any()

            # Return the result of the test #

            return is_in_keep_only_dataframe

    ### NUMBER OF VARIABLES' TEST FAILED ###

    else:

        return False


#########################################
#### GETTING THE AREACELLA DICTIONARY ###
#########################################


def get_areacella_apart(catalog, grouped_models: pd.Series) -> dict:
    """
    ---

    ### DEFINITION ###

    This function loads an areacella dictionary for every single entry of the catalog.

    ---

    ### INPUTS ###

    CATALOG : intake-esgf object | catalog allowing to do the search thanks to the ESGF API.

    GROUPED_MODELS : Pandas Series object | the entries grouped by (SOURCE_ID | MEMBER_ID | GRID_LABEL)

    ---

    ### OUTPUTS ###

    DICT_AREACELLA : DICT | hold an areacella xarray data array for every entry in the catalog

    ---

    """

    ### INITIALISATION  ###

    ## Initialise the full dictionary ##

    dict_areacella = {}

    ## Number of rows ##

    n_rows = grouped_models.size

    ### GO THROUGH EVERY ROW OF THE PANDA SERIES ###

    for ii in range(n_rows):

        ## Get the SOURCE_ID | MEMBER_ID | GRID_LABEL of the row ##

        # Retrieve the row ##

        row_ii = grouped_models.index[ii]

        # Extract the labels #

        source_id, member_id, grid_label = row_ii

        # Build the key for this dictionary entry ##

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

        print("\nDownloading areacella for {} ...\n".format(full_key))

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

        # Store it in dictionary #

        dict_areacella[full_key] = areacella_ii["areacella"]

    return dict_areacella


################################################
### FUNCTION TO DOWNLOAD ONE ENTRY AT A TIME ###
################################################


def generate_single_model_search_criterias(
    search_facets: dict,
    grouped_models_dataframe: pd.DataFrame,
    index: int,
) -> tuple[dict, str]:
    """
    ---

    ### DEFINITION ###

    This function generates search_criterias for a single entry of grouped_models_dataframe precising
    the (source_id, member_id, grid_label) criterias needed to download only one entry.

    ---

    ### INPUTS ###

    SEARCH_FACETS :  DICT | the original search facets dictionary

    GROUPED_MODELS_DATAFRAME : PANDAS DATAFRAME | the entries dels that have been grouped together by source_id, member_id and grid_label

    INDEX : INT | selected row index

    ---

    ### OUTPUTS ###

    SEARCH_CRITERIAS_GIVEN_ROW : DICT | search criterias updated with the source_id, member_id and grid_label criterias of the given row.

    SINGLE_MODEL_NAME : str | name of the single model we set the download for

    ---

    """

    ### COPYING THE ORIGINAL SEARCH CRITERIAS DICTIONARY ###

    search_criterias_given_row = search_facets.copy()

    ## Get the row information ##

    # Source_id #

    source_id_to_download = grouped_models_dataframe.iloc[index].source_id

    # Member_id #

    member_id_to_download = grouped_models_dataframe.iloc[index].member_id

    # Grid_label #

    grid_label_to_download = grouped_models_dataframe.iloc[index].grid_label

    ## Update the search criterias ##

    # Source_id #

    search_criterias_given_row["source_id"] = source_id_to_download

    # Member_id #

    search_criterias_given_row["member_id"] = member_id_to_download

    # Grid_label #

    search_criterias_given_row["grid_label"] = grid_label_to_download

    ## Generate the single model name ##

    single_model_name = (
        source_id_to_download
        + "."
        + member_id_to_download
        + "."
        + grid_label_to_download
    )

    return search_criterias_given_row, single_model_name


##########################################################################
### FUNCTION TO UPDATE THE KEYS OF THE DOWNLOADED ONE ENTRY DICTIONARY ###
##########################################################################


def update_single_entry_keys(
    single_model_dictionary: dict,
    single_model_name: str,
) -> dict:
    """

    ---

    ### DEFINITION ###

    This function updates the single entry keys of the downloaded one entry dictionary to allow to concatenate all dictionaries together :

    (experiment.variable) -> (source_id.member_id.grid_label.experiment.variable)

    ---

    ### INPUTS ###

    SINGLE_MODEL_DICTIONARY :  DICT | the downloaded single_model_dictionary with its keys under the form (experiment.variable)

    SINGLE_MODEL_NAME : STR | the name of the downloaded model under the form (source_id.member_id.grid_label)

    ---

    ### OUTPUTS ###

    SINGLE_MODEL_DICTIONARY : DICT | the updated single_model_dictionary with its keys under the form (source_id.member_id.grid_label.experiment.variable)

    ---

    """

    ### INITIALIZE ###

    ## Extract the dictionary keys ##

    # We transform the keys into a list such that old_keys do not change during the loop #

    old_keys = list(single_model_dictionary.keys())

    ### UPDATING THE KEYS ###

    for experiment_dot_variable in old_keys:

        ## Changing from (experiment.variable) to (source_id.member_id.grid_label.experiment.variable) ##

        new_key = single_model_name + "." + experiment_dot_variable

        ## Updating the keys ##

        single_model_dictionary[new_key] = single_model_dictionary.pop(
            experiment_dot_variable
        )

    return single_model_dictionary


###########################
#### LOADING CMIP6 DATA ###
###########################


def loading_cmip6(
    parent_path: str,
    downloading_folder_name: str,
    case: "str",
    do_we_clear: bool = False,
    remove_ensembles: bool = False,
    verbose : bool = False
) -> dict:
    """
    ---

    ### DEFINITION ###


    This function loads the CMIP6 data ensemble under the form of a dictionary structure.

    ---

    ### INPUTS ###

    PARENT_PATH : STR | path of the parent directory of the download folder

    DOWNLOADING_FOLDER_NAME : STR | name to be given to the download folder

    CASE : STR | defines the case for the search :

    - SW (short-wave variables for the APRP method)
    - ZELINKA-SW (short-wave variables for the APRP method by keeping only the models and variants present in Zelinka and al. (2023))

    DO_WE_CLEAR : BOOL | option to clear the downloading folder if it already exists

    REMOVE_ENSEMBLES : BOOL | option to keep only one variant per model

    ---

    ### OUTPUTS ###

    FULL_CMIP6_DICT : dictionary | hold a xarray data array for every variable of every single entry in the catalog

    SEARCH_DATAFRAME : pandas dataframe | hold all the information about the found entries

    AREACELLA_DICT : dictionary | hold an areacella xarray data array for every entry in the catalog

    ---
    """

    ### SET THE DOWNLOADING FOLDER ###

    set_downloading_folder(
        parent_path=parent_path,
        downloading_folder_name=downloading_folder_name,
        do_we_clear=do_we_clear,
    )

    ### INITIALIZE THE CATALOG ###

    ## Define it ##

    catalog = intake_esgf.ESGFCatalog()

    ## Looking at all the available nodes ##

    with intake_esgf.conf.set(
        all_indices=True
    ):  # with statement needed to make it work when the function is called

        ### SET THE CHOSEN CASE ###

        ## Defining some variables model wide ##

        # The criterias #

        global expected_number_of_files, filtering_by_name, keep_only_dataframe

        ## Get the criterias ##

        search_criterias = set_search_criterias(
            case
        )  # it's a dictionary with all the needed global search criterias to set

        ## Get the search facets ##

        search_facets = search_criterias["search_facets"]

        ## Get the expected number of files ##

        expected_number_of_files = search_criterias["expected_number_of_files"]

        ## Do we filter the models we keep by source_id and member_id ? ##

        # Boolean #

        filtering_by_name = search_criterias["filtering_by_name"]

        # The associated dataframe #

        keep_only_dataframe = search_criterias["keep_only_dataframe"]

        print("The search criterias are : {}\n".format(search_facets))

        ### SET THE SEARCH CRITERIAS (defined globally in this script) ###

        print("Filling the catalog with the search criterias...\n")

        catalog.search(
            **search_facets,
        )

        ### REMOVE THE INCOMPLETE ENTRIES ###

        print("Current found entries :\n \n{}\n".format(catalog.model_groups()))

        print("Removing the incomplete entries according to the case chosen...\n")

        catalog = catalog.remove_incomplete(filtering_function)

        ### DO WE KEEP ONLY ONE VARIANT PER MODEL ? ###

        if remove_ensembles:

            catalog = catalog.remove_ensembles()

        ### EXTRACT THE FINAL RESULTS OF THE SEARCH ###

        print("Therefore downloading and/or loading the following data dictionary:\n")

        print("\n{}\n".format(catalog.model_groups()))

        ## Generate the full dataframe of the files found by the search ##

        selected_entries_full_dataframe = catalog.df

        ## Save the grouped model pandas series for areacella downloading ##

        series_grouped_models = catalog.model_groups()

        ### GENERATE THE DATAFRAME FOR DOWNLOADING ONE ENTRY AT A TIME ###

        ## We extract the (source_id, member_id, grid_label) tuples from the full dataframe ##

        # We remove the duplicates to only keep one row per tuple #

        grouped_models_dataframe = (
            selected_entries_full_dataframe[["source_id", "member_id", "grid_label"]]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        ### DOWNLOAD EVERY SINGLE ENTRY AND COMBINE THEM INTO A DICTIONARY ###

        ## Initialize the full dictionary ##

        full_cmip6_dict = {}

        ## Downloading all the models one entry at a time ##

        print("Downloading and/or loading the data one entry at a time...\n")

        for index in grouped_models_dataframe.index:

            ## Reset the catalog ##

            catalog = intake_esgf.ESGFCatalog()

            ## Generate the associated search criterias ##

            search_criterias_given_row, single_model_name = (
                generate_single_model_search_criterias(
                    search_facets=search_facets,
                    grouped_models_dataframe=grouped_models_dataframe,
                    index=index,
                )
            )

            ## Generate the single model's output name ##

            print("\nDownloading {} ...\n".format(single_model_name))

            ## Display or not warnings for servers' connections ##

            if not verbose : 

                with warnings.catch_warnings():
            
                    ## Apply the search criterias ##

                    catalog.search(
                        **search_criterias_given_row,
                    )

                    ## Downloading the output... ##

                    single_model_dictionary = catalog.to_dataset_dict(
                        add_measures=False,
                        ignore_facets=[
                            "project",
                            "mip_era",
                            "activtity_drs",
                            "institution_id, table_id",
                            "grid_label",
                            "version",
                        ],
                        quiet=True,
                    )

            ## We keep the warnings ##

            else :

                ## Apply the search criterias ##

                    catalog.search(
                        **search_criterias_given_row,
                    )

                    ## Downloading the output... ##

                    single_model_dictionary = catalog.to_dataset_dict(
                        add_measures=False,
                        ignore_facets=[
                            "project",
                            "mip_era",
                            "activtity_drs",
                            "institution_id, table_id",
                            "grid_label",
                            "version",
                        ],
                        quiet=True,
                    )

            ## Updating its keys ##

            single_model_dictionary = update_single_entry_keys(
                single_model_dictionary, single_model_name
            )

            ## Updating the full dictionary ##

            full_cmip6_dict = full_cmip6_dict | single_model_dictionary

        ### LOAD THE AREACELLA DICTIONARY APART THANKS TO THE CATALOG ###

        print("Downloading and/or loading the areacella dictionary...\n")

        areacella_dict = get_areacella_apart(
            catalog, grouped_models=series_grouped_models
        )

    return full_cmip6_dict, areacella_dict


######################
### USED FOR TESTS ###
######################

if __name__ == "__main__":

    pass
