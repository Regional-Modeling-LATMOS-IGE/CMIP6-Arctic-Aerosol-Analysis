#!/usr/bin/env python3

"""
This small library is useful for the notebooks found in the download folder.
It holds several functions that call for bash procedures and [...]

Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""

##################################
### IMPORTATION OF THE MODULES ###
##################################

import os  # to handle path's management

import subprocess  # to run the wget code from python

#############################################
### DEFINITION OF THE SPECIFIC EXCEPTIONS ###
#############################################

class InputPathError(Exception):
    ''' Raise when the parent path ends with a '/' or the child path starts with a '/' '''

###################################
### DEFINITION OF THE FUNCTIONS ###
###################################


# ================ CREATE_DIR ================ #

def create_dir(parent_dir : str, to_be_created_dir : str) :

    """
    ### DEFINITION

    This function creates the directories we need for the downloading part calling bash routines.
    WARNING : This wont work if you put your '/' wildly. At the end of a given path there should be not '/'.
    
    ### INPUTS 

    PARENT_DIR : STR | parent directory of the to be created directory : it must exist or an error will be sent
    
    TO_BE_CREATED_DIR : STR | the directory that is to be created : it can be a folder or a path. 
    if it's a path, several folders and subfolders will be created.

    ### OUTPUT

    FULL_PATH : STR | the full path of the folders and maybe subfolders created.
    """

    ### WE DEFINE THE FULL PATH ###

    ## We try to define the full_path variable ##
    
    # We check that at the end of parent_dir there is no '/' #

    try :

        # If the end of parent_dir there is '/' we raise an error #
        
        if parent_dir[-1] == '/' :

            raise InputPathError

        elif to_be_created_dir[0] == '/' :

            raise InputPathError

        else :

            full_path = parent_dir + "/" + to_be_created_dir
            
    except InputPathError as error :

        raise InputPathError("neither parent_dir variable should end with a '/' nor to_be_created_dir variable start with a '/'")
        
    ### WE TRY TO MAKE THE FOLDER ###
    
    ## We try to make the folder but it will raise an error if parent_dir is wrong ##
    
    try : 
    
        ## We first check if to_be_created_dir already exists or not ##
    
        # If it exists : we remove it #
        
        if os.path.isdir(full_path) :
    
            # We run the rm -rf command from python to erase the folder and its content #
    
            subprocess.run(
            "rm -rf {}".format(full_path), shell=True, check=True
        )
            print("Pre-existing folder at {} removed".format(full_path))
        
        ## We run the mkdir command from python to make the folder ##
            
        subprocess.run(
            "mkdir  -p {}".format(full_path), shell=True, check=True  # -p option allows for simultaneous folder and subfolder creation
        )
    
        print("New folder at {} created".format(full_path))
    
    ## An error was caught : storage_dir does not exist ##
    
    except FileNotFoundError as error:
    
        print("The storage_dir variable is wrong, such a path does not exists" + " : " + parent_dir + "\n")
    
        raise 

    return full_path

# ================ MV_DOWNLOADED_DATA ================ #

def mv_downloaded_data(current_dir : str ,future_dir : str) :

    """
    ### DEFINITION

    This function moves the downloading folder in cuto the future_dir folder
    WARNING : This wont work if you put your '/' wildly. At the end of a given path there should be not '/'.
    
    ### INPUTS 

    PARENT_DIR : STR | parent directory of the to be created directory : it must exist or an error will be sent
    
    TO_BE_CREATED_DIR : STR | the directory that is to be created : it can be a folder or a path. 
    if it's a path, several folders and subfolders will be created.

    ### OUTPUT

    FULL_PATH : STR | the full path of the folders and maybe subfolders created.
    """

    ### WE DEFINE THE FULL PATH ###

    ## We try to define the full_path variable ##
    
    # We check that at the end of parent_dir there is no '/' #

    try :

        # If the end of parent_dir there is '/' we raise an error #
        
        if parent_dir[-1] == '/' :

            raise InputPathError

        elif to_be_created_dir[0] == '/' :

            raise InputPathError

        else :

            full_path = parent_dir + "/" + to_be_created_dir
            
    except InputPathError as error :

        raise InputPathError("neither parent_dir variable should end with a '/' nor to_be_created_dir variable start with a '/'")
        
    ### WE TRY TO MAKE THE FOLDER ###
    
    ## We try to make the folder but it will raise an error if parent_dir is wrong ##
    
    try : 
    
        ## We first check if to_be_created_dir already exists or not ##
    
        # If it exists : we remove it #
        
        if os.path.isdir(full_path) :
    
            # We run the rm -rf command from python to erase the folder and its content #
    
            subprocess.run(
            "rm -rf {}".format(full_path), shell=True, check=True
        )
            print("Pre-existing folder at {} removed".format(full_path))
        
        ## We run the mkdir command from python to make the folder ##
            
        subprocess.run(
            "mkdir  -p {}".format(full_path), shell=True, check=True  # -p option allows for simultaneous folder and subfolder creation
        )
    
        print("New folder at {} created".format(full_path))
    
    ## An error was caught : storage_dir does not exist ##
    
    except FileNotFoundError as error:
    
        print("The storage_dir variable is wrong, such a path does not exists" + " : " + parent_dir + "\n")
    
        raise 

    return full_path


if __name__ == '__main__':
    pass