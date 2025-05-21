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

from utilities.tools_for_analysis.handle_data.extract_one_variant_per_model import (
    extract_source_id_from_str, # to extract the source id from a key
)

############################################
### TESTS FOR EXTRACT_SOURCE_ID_FROM_STR ###
############################################

def test_correct_source_id_retrieved():
    assert extract_source_id_from_str("ACCESS-CM2.r1i1p1f1.gn") == "ACCESS-CM2"

############################################
### TESTS FOR EXTRACT_SOURCE_ID_FROM_STR ###
############################################
