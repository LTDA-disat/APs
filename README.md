# APs
Python implementation of the Apparent Thermal Inertia of Snow (APs).

## Overview

The Apparent Thermal Inertia of Snow (APs) has been used to monitor snowmelt dynamics and identify the onset of snowmelt phases from meteorological observations.
APs is derived from surface albedo, surface temperature, incoming shortwave radiation and seasonal variations in solar illumination.

This implementation computes daily APs values from meteorological station data and site latitude.


## Installation

Clone the repository:

```bash
git clone https://github.com/LTDA-disat/APs.git
cd APs
```

Create a dedicated Conda environment:

```bash
conda create -n aps python=3.11
conda activate aps
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Repository structure

```text
APs/
│
├── aps.py
├── solar.py
├── example.py
├── README.md
│
├── input/
│   └── example_meteo.csv
│
└── output/
    └── APs_output.xlsx
```

### Files

- `aps.py` contains the APs computation routine.
- `solar.py` contains the calculation of solar declination and the seasonal solar illumination term.
- `example.py` provides a complete working example.
- `example_meteo.csv` is an example meteorological dataset.
- `APs_output.xlsx` is an example output file.


## Required input data

The APs algorithm requires a meteorological dataset containing:

| Column | Description | Units |
|----------|----------|----------|
| datehour | Date and time of the observation | datetime |
| Albedo | Surface albedo | - |
| tsur_spl | Surface snow temperature | °C |
| swin | Incoming shortwave radiation | W m⁻² |

The input file can be provided as a CSV file.

Example:

| datehour | Albedo | tsur_spl | swin |
|-----------|---------|----------|------|
| 2017-12-01 00:00 | 0.89 | -6.3 | 0 |
| 2017-12-01 00:30 | 0.89 | -6.5 | 0 |
| 2017-12-01 01:00 | 0.89 | -6.6 | 0 |
| ... | ... | ... | ... |


The user must provide also:

- latitude (decimal degrees)

## Output

The function returns a `pandas.DataFrame` with the following fields:

| Column | Description |
|----------|----------|
| `date` | Date |
| `Alb` | Mean albedo (13:00–15:00) |
| `Tsur5` | Mean surface temperature (04:00–06:00) |
| `Tsur14` | Mean surface temperature (13:00–15:00) |
| `DTsur` | Temperature difference (`Tsur14 - Tsur5`) |
| `SWin` | Daily mean incoming shortwave radiation |
| `APs` | Apparent Thermal Inertia of Snow |


## Citation

If you use this software in scientific work, please cite:

Gatti, O., Di Mauro, B., Marin, C., Garzonio, R., Bianchi, G., Pogliotti, P., Notarnicola, C., Pettinato, S., Cremonese, E., & Colombo, R.

*Combined use of radar remote sensing, apparent thermal inertia and snowpack modelling to characterize snowmelt phases in Alpine environments.*

Frontiers in Remote Sensing.

Additionally, please cite the original APs formulation:

Colombo, R., Garzonio, R., Di Mauro, B., Dumont, M., Tuzet, F., Cogliati, S., Pozzi, G., Maltese, A., & Cremonese, E. (2019).

*Introducing Thermal Inertia for Monitoring Snowmelt Processes With Remote Sensing.*

Geophysical Research Letters, 46(8).

https://doi.org/10.1029/2019GL082193

## License

MIT License


