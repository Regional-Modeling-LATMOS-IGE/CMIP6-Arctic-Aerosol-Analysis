#!/usr/bin/env python3

"""
This script is used to perform regridding on a common grid for a bunch of the CMIP6 outputs.
We create a common grid based on the coarser resolutions accessible in the ensemble and transform all the intensive
variables into extensive variables upon regridding thanks to the areacella variable present in the datasets.

Author : GIBONI Lucas

Feel free to copy, adapt and modify it under the provided license on github.
"""
