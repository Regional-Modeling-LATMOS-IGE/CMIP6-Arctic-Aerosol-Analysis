#!/usr/bin/env python3

"""
This submodule is made to be able to extract only one variant per model
Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""

##################################
### IMPORTATION OF THE MODULES ###
##################################

### DATA OBJECTS AND ASSOCIATED COMPUTATION ###

import numpy as np  # to handle numpy arrays and the associated tools

#########################################
### EXTRACT THE SOURCE ID FROM A KEY ####
#########################################


def extract_source_id_from_str(key: str) -> str:
    """

    ---

    ### DEFINITION ###

    This function takes a key and extracts the associated source_id.

    ---

    ### INPUTS ###

    KEY : STR | a key associated to one entry of the dictionary

    ---

    ### OUTPUTS ###

    SOURCE_ID : STR | the extracted source_id

    ---

    """

    ### CHECK INPUT TYPE ###

    if not isinstance(key, str):

        raise TypeError("expected a string")

    ### GENERATES THE SPLITTED KEY ###

    splitted_key = key.split(".")

    ### FINDS THE SOURCE ID ###

    source_id = splitted_key[0]

    return source_id


######################################################
### OBTAIN THE SOURCE_ID LIST FROM THE KEYS' LIST ####
######################################################


def get_source_id_from_keys_list(keys_list: list[str]) -> list[str]:
    """
    ---

    ### DEFINITION ###

    This function takes the keys' lists and transforms it in a source id list.

    ---

    ### INPUTS ###

    KEYS_LIST : LIST[STR] | the keys' list of the models' output dictionary

    ---

    ### OUTPUTS ###

    SOURCE_ID_LIST : LIST[STR] | the extracted source_id list

    ---


    """

    ### CHECK INPUT TYPE ###

    ## Is the input a list ? ##

    if not isinstance(keys_list, list):

        raise TypeError("expected a list")

    ## Are the elements of the list only str ? ##

    if not all(isinstance(element, str) for element in keys_list):

        raise TypeError("expected an only string list")

    ### GENERATE THE SOURCE_ID LIST ###

    source_id_list = [extract_source_id_from_str(key) for key in keys_list]

    return source_id_list


#######################################################################################
### FIND THE FIRST INDEX THAT CORRESPONDS TO A GIVEN SOURCE ID IN A SOURCE_ID LIST ####
#######################################################################################


def find_first_index_for_given_source_id(
    given_source_id: str, source_id_list: list[str]
) -> int:
    """

    ---

    ### DEFINITION ###

    This function finds the first index that corresponds to given_source_id in a source_id list.

    ---

    ### INPUTS ###

    GIVEN_SOURCE_ID : STR | the given source_id we look for in the list

    SOURCE_ID_LIST : LIST[STR] | list of all the source_id

    ---

    ### OUTPUTS ###

    FIRST_INDEX : INT | the first corresponding index to given_source_id

    ---

    """

    ### CHECK INPUT TYPE ###

    ## Is given_source_id a str ##

    if not isinstance(given_source_id, str):

        raise TypeError("expected a string")

    ## Is source_id_list a list ? ##

    if not isinstance(source_id_list, list):

        raise TypeError("expected a list")

    ## Are all the elements of the list string ? ##

    if not all(isinstance(element, str) for element in source_id_list):

        raise TypeError("expected an only string list")

    ### FIND THE FIRST INDEX ###

    ## Generates an index_list that corresponds to the index where there is a match with given_source_id ##

    index_list = [
        i for i, source_id in enumerate(source_id_list) if source_id == given_source_id
    ]

    ## Select the first index ##

    first_index = index_list[0]

    return first_index


############################################################################
### GET ONLY ONE VARIANT PER SOURCE ID FOR EVERY ENTRY IN THE KEYS_LIST ####
############################################################################


def extract_only_one_variant_keys_list(keys_list: list[str]) -> list[str]:
    """

    ---

    ### DEFINITION ###

    This function takes the keys' list of the entries' dictionary and conserves only one variant per source id.

    ---

    ### INPUTS ###

    KEYS_LIST : LIST[STR] | the keys' list of the models' output dictionary

    ---

    ### OUTPUTS ###

    ONLY_ONE_VARIANT_KEYS_LIST : LIST[STR] | a new keys' list for selecting only one variant per source id in the dictionary entry

    ---

    """

    ### CHECK INPUT TYPE ###

    ## Is the input a list ? ##

    if not isinstance(keys_list, list):

        raise TypeError("expected a list")

    ### GENERATE THE SOURCE_ID LIST ###

    ## Extract the source_id from every key ##

    source_id_list = get_source_id_from_keys_list(keys_list)

    ## Remove the duplicates ##

    unique_source_id_list = np.unique(source_id_list)

    ### IDENTIFY THE INDEXES TO KEEP ###

    index_to_keep = [
        find_first_index_for_given_source_id(
            given_source_id=given_source_id, source_id_list=source_id_list
        )
        for given_source_id in unique_source_id_list
    ]

    ### SELECT THE ENTRIES' KEYS THAT WE PRESERVE ###

    only_one_variant_keys_list = [keys_list[index] for index in index_to_keep]

    return only_one_variant_keys_list
