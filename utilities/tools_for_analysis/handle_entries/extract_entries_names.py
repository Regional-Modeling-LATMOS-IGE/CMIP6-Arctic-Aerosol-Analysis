#!/usr/bin/env python3

"""
This submodule is made to be able to the entries' names without the experiments
Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""


####################################################
### GENERATE THE ENTRIES WITHOUT THE EXPERIMENTS ###
####################################################


def get_entries_only_from_clim_dict(key_with_exp: str) -> str:
    """
    ---
    ### DEFINITION ###

    This function receives a key from the climatology dictionary and removes the experiment at the end to generate an only model and variants list.

    ---
    ### INPUTS ###

    KEY_WITH_EXP : STR | key of the climatology dictionary holding the experiment specification at the end.

    ---
    ### OUTPUTS ###

    KEY_WITHOUT_EXP : STR | input key deprived of the experiment specification
    ---
    """

    ### CHECK INPUT TYPE ###

    if not isinstance(key_with_exp, str):

        raise TypeError("expected a string")

    ### REMOVE THE EXPERIMENT ###

    ## Split the key into a list of str ##

    splitted_key = key_with_exp.split(".")

    ## Remove the experiment specification at the end ##

    splitted_key_without_exp = splitted_key[:-1]

    ## Rejoin the newly formed key ##

    key_without_exp = ".".join(splitted_key_without_exp)

    return key_without_exp