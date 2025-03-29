# Downloading script's dev branch

Developing a downloading script for the whole CMIP6 data and an example for reproducibility.

## Content of the repository for this branch

The folder */utilities* holds the different scripts used to download and pre-treat the CMIP6 data used for this analysis.\
The notebook held in */utilities/download/* that is named *download_cmip6.ipynb* shows how we use the **intake-esgf** package ([https://github.com/esgf2-us/intake-esgf?tab=readme-ov-file](https://github.com/esgf2-us/intake-esgf)) to download and load the CMIP6 datasets we need. What's more, the notebook holds a routine that allows for a fast downloading and loading of the areacella variable for every single downloaded model entry. Indeed, the package tends to be quit slow when doing it natively on the large model ensemble we need.

## Reference of the downloaded data

The intake-esgf library allows us to retrieve the **tracking_id** of every entry we download (https://intake-esgf.readthedocs.io/en/latest/reproduce.html). 




