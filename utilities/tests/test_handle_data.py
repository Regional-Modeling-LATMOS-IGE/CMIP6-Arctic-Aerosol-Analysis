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
    extract_source_id_from_str,  # to extract the source id from a key
    get_source_id_from_keys_list,  # to generate the source_id list
    find_first_index_for_given_source_id,  # finds the first index corresponding to a given source_id in a source_id list
    extract_only_one_variant_keys_list,  # generates the keys' list with only one variant per source id
)

### TEST MODULE ###

import pytest

############################################
### TESTS FOR EXTRACT_SOURCE_ID_FROM_STR ###
############################################


def test_error_if_wrong_type_extract_source_id_from_str():
    with pytest.raises(TypeError):
        extract_source_id_from_str(3)


def test_correct_source_id_retrieved_extract_source_id_from_str():
    assert extract_source_id_from_str("ACCESS-CM2.r1i1p1f1.gn") == "ACCESS-CM2"


##############################################
### TESTS FOR GET_SOURCE_ID_FROM_KEYS_LIST ###
##############################################


def test_error_if_wrong_type_get_source_id_from_keys_list():
    with pytest.raises(TypeError):
        get_source_id_from_keys_list(3)


def test_error_if_wrong_type_in_list_get_source_id_from_keys_list():
    with pytest.raises(TypeError):
        get_source_id_from_keys_list(["ACCESS-CM2", 3])


def test_correct_source_id_list_retrieved_get_source_id_from_keys_list():
    assert get_source_id_from_keys_list(
        ["ACCESS-CM2.r1i1p1f1.gn", "ACCESS-ESM1-5.r1i1p1f1.gn"]
    ) == ["ACCESS-CM2", "ACCESS-ESM1-5"]


######################################################
### TESTS FOR FIND_FIRST_INDEX_FOR_GIVEN_SOURCE_ID ###
######################################################


def test_error_if_wrong_type_given_source_id_find_first_index_for_given_source_id():
    with pytest.raises(TypeError):
        find_first_index_for_given_source_id(
            given_source_id=3, source_id_list=["ACCESS-CM2", "ACCESS-ESM1-5"]
        )


def test_error_if_wrong_type_source_id_list_find_first_index_for_given_source_id():
    with pytest.raises(TypeError):
        find_first_index_for_given_source_id(
            given_source_id="ACCESS-CM2", source_id_list=3
        )


def test_error_if_wrong_type_in_list_find_first_index_for_given_source_id():
    with pytest.raises(TypeError):
        find_first_index_for_given_source_id(
            given_source_id="ACCESS-CM2", source_id_list=["ACCESS-CM2", 3]
        )


def test_correct_index_retrieved_find_first_index_for_given_source_id():
    assert (
        find_first_index_for_given_source_id(
            given_source_id="ACCESS-ESM1-5",
            source_id_list=[
                "ACCESS-CM2",
                "ACCESS-ESM1-5",
                "ACCESS-ESM1-5",
                "ACCESS-CM2",
            ],
        )
        == 1
    )


####################################################
### TESTS FOR EXTRACT_ONLY_ONE_VARIANT_KEYS_LIST ###
####################################################


def test_error_if_wrong_type_extract_only_one_variant_keys_list():
    with pytest.raises(TypeError):
        extract_only_one_variant_keys_list(3)


def test_error_if_wrong_type_in_list_extract_only_one_variant_keys_list():
    with pytest.raises(TypeError):
        extract_only_one_variant_keys_list(["ACCESS-CM2", 3])


def test_correct_index_retrieved_extract_only_one_variant_keys_list():
    assert extract_only_one_variant_keys_list(
        [
            "IPSL-CM6A-LR.r1i1p1f1.gr",
            "IPSL-CM6A-LR.r2i1p1f1.gr",
            "IPSL-CM6A-LR.r3i1p1f1.gr",
            "IPSL-CM6A-LR.r4i1p1f1.gr",
            "IPSL-CM6A-LR-INCA.r1i1p1f1.gr",
            "MIROC6.r11i1p1f1.gn",
            "MIROC6.r1i1p1f1.gn",
        ]
    ) == [
        "IPSL-CM6A-LR.r1i1p1f1.gr",
        "IPSL-CM6A-LR-INCA.r1i1p1f1.gr",
        "MIROC6.r11i1p1f1.gn",
    ]
