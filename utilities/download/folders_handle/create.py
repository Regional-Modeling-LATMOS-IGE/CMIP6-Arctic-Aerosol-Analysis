#!/usr/bin/env python3

"""
This small library is useful for the notebooks found in the download folder.

Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""

##################################
### IMPORTATION OF THE MODULES ###
##################################

import os  # to handle path's management

import shutil  # to handle the removal of a folder tree


#############################################
### DEFINITION OF THE SPECIFIC EXCEPTIONS ###
#############################################


class FileExistsError(Exception):
    """Raise when the path already exists and isn't a regular file or folder"""


###################################
### DEFINITION OF THE FUNCTIONS ###
###################################


# ================ CREATE_DIR ================ #


def create_dir(parent_path: str, name: str, clear: bool = True) -> str:
    """
    ### DEFINITION ###

    Create the entire chain of folders and optionally empty the contents of the last one or delete the file with this name.

    ### INPUTS ###

    PARENT_PATH : STR | path of the parent directory of the to be created structure

    NAME : STR | the structure that is to be created : it can be a folder, a path or a symbolic link.
    If it is a path, the whole tree will be created.

    CLEAR : STR | boolean to define if we clear the structure if it already exists.
    default : True

    ### OUTPUT ###

    PATH : STR | the full path of the folders and maybe subfolders created.
    """

    ### CREATE THE FULL PATH ###

    path = os.path.join(parent_path, name)

    ### CLEARING PROCEDURE IF THE PATH/SYMLINK ALREADY EXISTS ###

    ## Test if we need to clear and if the path/symlink already exists ##

    if clear and os.path.lexists(path):

        ## If it is a path or a symlink we remove it ##

        if os.path.isfile(path) or os.path.islink(path):

            shutil.rmtree(path)

        ## If it is a path we remove all the tree ##

        elif os.path.isdir(path):
            
            shutil.rmtree(path)

        ## If we do not know what this is ##

        else:
            raise FileExistsError(
                "Path already exists and isn't a regular file or folder"
            )

    ### MAKE THE DIRECTORY ###

    os.makedirs(path, exist_ok=True)  # if it exists : no error is sent

    return path


######################
### USED FOR TESTS ###
######################

if __name__ == "__main__":
    pass
