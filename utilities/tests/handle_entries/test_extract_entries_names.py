#!/usr/bin/env python3

"""
Test library for extract_one_variant_per_model.py

Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""

##################################
### IMPORTATION OF THE MODULES ###
##################################

### MODULE TO BE TESTED ###

from utilities.tools_for_analysis.handle_entries.extract_entries_names import (
    get_entries_only_from_clim_dict, # creates an only model and variants list
)

### TEST MODULE ###

import pytest


#######################################
### GET ENTRIES ONLY FROM CLIM DICT ###
#######################################

def test_error_if_wrong_type_get_entries_only_from_clim_dict():
    with pytest.raises(TypeError):
        get_entries_only_from_clim_dict(
            key_with_exp = 3
        )


def test_correct_model_variant_found_get_entries_only_from_clim_dict():
    assert (
        get_entries_only_from_clim_dict(
            key_with_exp="ACCESS-CM2.r1i1p1f1.gn.piClim-aer",
        )
        == "ACCESS-CM2.r1i1p1f1.gn"
    )
