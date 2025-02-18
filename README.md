# Assess the aerosol-cloud effective radiative forcing in the Arctic for CMIP6 models

Computation of the aerosol-cloud's interaction effective radiative forcing (ERF) for a subset of the CMIP6 model ensemble for the Arctic.

## Scientific purpose of the repository 

The Arctic is one of the fastest warming regions on the planet, with temperatures rising 4 times faster than the global average.
Half of the recent arctic warming since 1990 could be due to changes in aerosols, especially through their effects on cloud formation.
Despite their potential importance, the effect of the aerosol-cloud interactions on the ERF are highly uncertain for the Arctic. 

## Data used 

### Description

We use two experiments realized for the Coupled Model Intercomparison Project phase 6 (CMIP6)  : **piClim-control** and **piClim-aer**. These are both atmosphere-only climate model simulations in which sea surface temperatures (SSTs) and sea ice concentrations (SICs) are fixed at model-specific preindustrial climatological values. On the one hand, the piClim-control realization assumes aerosols' burdens set to their preindustrial levels hence why it is dubbed as the control experiment. On the other hand, the piClim-aer realization uses present-day, present-day being 2014, aerosols burdens' levels.

### Variables used

- **clt**  : Total cloud area fraction (%) for the whole atmospheric column

- **rsdt** : Shortwave radiation ($W/m^{2}$) **incident** at the TOA
 
- **rsut**: Shortwave radiation ($W/m^{2}$) **going out**  at the TOA

- **rsutcs** : Shortwave radiation ($W/m^{2}$) **going out**  at TOA for **clear-sky conditions**

- **rsds** : Shortwave **downwelling** radiation ($W/m^{2}$) at the surface
 
- **rsdscs**  : Shortwave **downwelling** radiation ($W/m^{2}$) at the surface for **clear-sky conditions**

- **rsus** : Shortwave **upwelling** radiation ($W/m^{2}$) at the surface

- **rsuscs** : Shortwave **upwelling** radiation ($W/m^{2}$) at the surface for **clear-sky conditions**


### References 

## Content of the repository

The folder */utilities* holds the different scripts used to download and pre-treat the CMIP6 data used for this analysis.
