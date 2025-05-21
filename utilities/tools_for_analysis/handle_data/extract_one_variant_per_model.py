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

def extract_source_id_from_str(key : str) -> str :
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

        ### GENERATES THE SPLITTED KEY ###

        splitted_key = key.split(".")

        ### FINDS THE SOURCE ID ###

        source_id = splitted_key[0]

        return source_id