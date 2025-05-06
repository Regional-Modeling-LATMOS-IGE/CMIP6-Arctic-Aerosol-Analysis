# ~/utilities/get_cmip6_data/prepare_data

## Description of the submodule :

This submodule is contributing to the pre-treatment of the datasets produced by the *store_data* submodule before the analysis.

### extract_climatologies.py

This python script is used to treat the raw CMIP6 data we have downloaded. We transfom the single variable datasets that span over the 30-year simulation 
period into monthly climatologies that are regrouped under the same model.variant hood. It uses the *store_data* submodule.

