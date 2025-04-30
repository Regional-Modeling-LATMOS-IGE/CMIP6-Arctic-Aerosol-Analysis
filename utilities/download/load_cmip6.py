#!/usr/bin/env python3

"""
This small script is used to load the CMIP6 data used for the analysis.
For more details on the methods employed in the script, please refer to the download_cmip6.ipynb notebook in the same folder.

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

import pandas as pd # to manage the product of the search

### HOMEMADE LIBRARIES ###

from utilities.download.folders_handle.create import (
    create_dir,
)  # function to create a cleaned downloading directory

#############################
#### DEFINE CUSTOM ERRORS ###
#############################

class InvalidCase(Exception):

    ### DEFINING THE EXCEPTION PROPERTIES ###

    def __init__(self, case, error_msg="The following case is not covered for the search"):
        self.case = case
        self.error_msg = error_msg
        super().__init__(self.msg) # calling the exception parent class

    ### DEFINING THE ERROR MESSAGE ###

    def __str__(self): # what happens when printing the error
        return f'{self.case} -> {self.error_msg}'
    
#############################################
#### DEFINE GLOBALLY THE SEARCH CRITERIAS ###
#############################################

def set_search_criterias(case : str) -> dict:
    """

    ### DEFINITION ###

    This function allows us to define dynamically the search criterias in function of the case we are in.

    ### INPUTS ###

    CASE : STR | str defining the case for the search :
    
    - SW (short-wave variables for the APRP method)
    - ZELINKA-SW (short-wave variables for the APRP method by keeping only the models and variants present in Zelinka and al. (2023))

    ### OUTPUTS ###

    SEARCH : DICT | dictionnary holding the search criterias

    EXPECTED_NUMBER_OF_FILES : INT | expected number of files such that on model_id and source_id couples corresponds to (number_of_variables) * (number_of_experiments)

    ### REFERENCES ###

    Zelinka, M. D., Smith, C. J., Qin, Y., and Taylor, K. E.: Comparison of methods to estimate aerosol effective radiative forcings in climate models, 
    Atmos. Chem. Phys., 23, 8879–8898, https://doi.org/10.5194/acp-23-8879-2023, 2023.

    """

    ### SHORT-WAVE ONLY CASE ###

    if case == "SW" :

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

        ### DEFINE SEARCH CRITERIAS DICTIONNARY ###

        search = {
            "experiment_id" : experiment_id,
            "variable_id" : variable_id,
            "table_id" : table_id
        }


        # ================ EXPECTED NUMBER OF FILES ================ #

        expected_number_of_files = 16 # 8 variables * 2 experiments

        return {'search' : search, 'expected_number_of_files' : expected_number_of_files, 'filtering_by_name' : False, 'keep_only_dataframe' : None}
    
    elif case == "ZELINKA-SW" :

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

        ### DEFINE SEARCH CRITERIAS DICTIONNARY ###

        search = {
            "experiment_id" : experiment_id,
            "variable_id" : variable_id,
            "table_id" : table_id
        }


        # ================ EXPECTED NUMBER OF FILES ================ #

        expected_number_of_files = 16 # 8 variables * 2 experiments

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
            "UKESM1-0-LL" 
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
            "r1i1p1f4"
        ]

        zelinka_2023_model_variant_table = pd.DataFrame({"source_id" : source_id_zelinka_2023, "member_id" : member_id_zelinka_2023}, dtype = str)

        return {'search' : search, 'expected_number_of_files' : expected_number_of_files, 'filtering_by_name' : True, 'keep_only_dataframe' : zelinka_2023_model_variant_table}

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

########################################################################################
#### FILTERING FUNCTION REMOVING INCOMPLETE ENTRIES AND KEEPING ONLY PROVIDED MODELS ###
########################################################################################


# ================ DEFINE THE FILTERING FUNCTION ================ #

def filtering_function(grouped_model_entry : pd.DataFrame) -> bool:
    """

    ### DEFINITION ###

    This function allows the intake-esgf catalog to be cleaned of the entries that are not complete.
    In the default case it means entries that do not meet the expected number of files. 

    The user can also set a condition that only the model and variant couples present in a provided pandas dataframe are kept.
    Since the nature of this function is to be an input for the intake-esgf package, we define the optional arguments outside
    of the function.

    ### INPUTS

    GROUPED_MODEL_ENTRY : Pandas DataFrame | sub dataframe containing all the variables of a given source_id, member_id and grid tuple.

    ### OPTIONAL ARGUMENTS (DEFINED GLOBALLY)

    FILTERING_BY_NAME : BOOL | defines if we filter the entry by source_id and member_id or not

    KEEP_ONLY_DATAFRAME : Pandas DataFrame | associated dataframe holding the source_id and member_id to conserve
    
    ### OUTPUTS

    BOOL | whether we keep this model group or not
    """

    ### INITIALISATION ###

    ### TEST THE NUMBER OF VARIBALES ###

    if len(grouped_model_entry) == expected_number_of_files:

        ### NUMBER OF VARIABLES' TEST SUCCEEDED ###

        ## Do we keep only the keep_only_dataframe model and variant couples ? ##

        # NO : We keep everything that matched the variable number's test #

        if not(filtering_by_name):

            return True
        
        ### YES : KEEPING ONLY THE COUPLES PRESENT IN KEEP_ONLY_DATAFRAME ###

        else :
            
            ## Doing the test on the grouped_model_entry's source_id and member_id ##

            # Extract the grouped_model_entry data #

            grouped_model_entry_source_id = grouped_model_entry.source_id.unique()[0]

            grouped_model_entry_member_id = grouped_model_entry.member_id.unique()[0]

            # Can we find the grouped_model_entry's source_id and member_id in one row of is_in_keep_only_dataframe ? #

            is_in_keep_only_dataframe = ((keep_only_dataframe['source_id'] == grouped_model_entry_source_id) 
            & (keep_only_dataframe['member_id'] == grouped_model_entry_member_id)).any()

            # Return the result of the test #

            return is_in_keep_only_dataframe
    
    ### NUMBER OF VARIABLES' TEST FAILED ###

    else :

        return False

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
    parent_path: str, downloading_folder_name: str, case : 'str', do_we_clear: bool = False
) -> dict:
    """
    ---

    ### DEFINITION ###

    
    This function loads the CMIP6 data ensemble under the form of a dictionnary structure.
    
    ---

    ### INPUTS ###
    
    PARENT_PATH : STR | path of the parent directory of the download folder

    DOWNLOADING_FOLDER_NAME : STR | name to be given to the download folder

    CASE : STR | defines the case for the search :
    
    - SW (short-wave variables for the APRP method)
    - ZELINKA-SW (short-wave variables for the APRP method by keeping only the models and variants present in Zelinka and al. (2023))

    DO_WE_CLEAR : BOOL | option to clear the downloading folder if it already exists

    ---

    ### OUTPUTS ###

    DICT_CMIP6 : dictionnary | hold a xarray data array for every variable of every single entry in the catalog

    SEARCH_DATAFRAME : pandas dataframe | hold all the information about the found entries

    DICT_AREACELLA : dictionnary | hold an areacella xarray data array for every entry in the catalog

    ---
    """

    ### SET THE DOWNLOADING FOLDER ###

    set_downloading_folder(
        parent_path=parent_path,
        downloading_folder_name=downloading_folder_name,
        do_we_clear=do_we_clear,
    )

    ### INITIALIZE THE CATALOG ###

    catalog = intake_esgf.ESGFCatalog()

    ### SET THE CHOSEN CASE ###

    ## The criterias are defined module wide ##

    global expected_number_of_files, filtering_by_name, keep_only_dataframe

    ## Get the criterias ##

    search_criterias = set_search_criterias(case) # it's a dictionnary with all the needed global search criterias to set

    ## Get the search facets ##

    search = search_criterias['search']

    ## Get the expected number of files ##

    expected_number_of_files = search_criterias['expected_number_of_files']

    ## Do we filter the models we keep by source_id and member_id ? ##

    # Boolean #

    filtering_by_name = search_criterias['filtering_by_name']

    # The associated dataframe #

    keep_only_dataframe = search_criterias['keep_only_dataframe']

    print("The search criterias are : {}\n".format(search))

    ### SET THE SEARCH CRITERIAS (defined globally in this script) ###

    print("Filling the catalog with the search criterias...\n")

    catalog.search(
        **search,
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
