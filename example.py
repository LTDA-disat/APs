# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:51:10 2026

@author: claudia.ravasio
"""

import pandas as pd
from aps import compute_aps

"""params"""
latitude = 45.844275

# APs parameters
t1 = 5 # Central time of the morning averaging window (05:00)
t2 = 14 # Central time of the afternoon averaging window (14:00)
tmax = 14 # Daily temperature maximum
half_window = 60 # Half-width of the averaging windows [minutes].

df = pd.read_csv("input/example_meteo.csv")

"""compute"""
aps = compute_aps(
    df,
    latitude,
    albedo_col="Albedo",
    tsur_col="tsur_spl",
    swin_col="swin",
    t1 = t1,
    t2 = t2,
    tmax = tmax,
    half_window = half_window)


"""save"""
aps.to_excel(
    "output/APs_output.xlsx",
    index=False,
    na_rep="NaN",
)

