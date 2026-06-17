# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:51:10 2026

@author: claudia.ravasio
"""

import pandas as pd
from aps import compute_aps

latitude = 45.844275

df = pd.read_csv("input/example_meteo.csv")

aps = compute_aps(df,latitude)

aps.to_excel(
    "output/APs_output.xlsx",
    index=False,
    na_rep="NaN"
)

print(aps.head())