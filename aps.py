# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:58:17 2026

@author: claudia.ravasio
"""

import numpy as np
import pandas as pd
from solar import compute_axec


def safe_nanmean(x):
    """
    Compute mean ignoring NaN values.

    Returns NaN if all values are missing.
    """
    if np.all(np.isnan(x)):
        return np.nan

    return np.nanmean(x)

def compute_aps(df, latitude):
    """
    Compute daily APs from meteorological observations.

    The calculation uses:
    - surface temperature averaged between 04:00 and 06:00
    - surface temperature averaged between 13:00 and 15:00
    - surface albedo averaged between 13:00 and 15:00
    - daily mean incoming shortwave radiation

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe containing:
            - datehour : datetime
            - Albedo
            - tsur_spl
            - swin

    latitude : float
        Site latitude in decimal degrees.

    Returns
    -------
    pandas.DataFrame
        Daily APS table.
    """
    
    df = df.copy()

    df["datehour"] = pd.to_datetime(df["datehour"])
    
    # Compute Axec automatically
    df["Axec"] = compute_axec(
        df["datehour"],
        latitude
    )
    
    # APS constants
    t1 = 5 * 3600  # reference morning time (05:00)
    t2 = 14 * 3600 # reference afternoon time (14:00)
    tmax = 14 * 3600 # assumed daily temperature maximum
    wvel = 7.27e-5 # Earth's angular velocity [rad s-1]

    bxec = np.tan(wvel * tmax) / (
        1 - np.tan(wvel * tmax)
    )

    results = []
    
    for date, dataday in df.groupby(df["datehour"].dt.date):

        mask_t1 = (
            ((dataday["datehour"].dt.hour == 4))
            |
            ((dataday["datehour"].dt.hour == 5))
            |
            (
                (dataday["datehour"].dt.hour == 6)
                &
                (dataday["datehour"].dt.minute == 0)
            )
        )

        # 13:00–15:00
        mask_t2 = (
            ((dataday["datehour"].dt.hour == 13))
            |
            ((dataday["datehour"].dt.hour == 14))
            |
            (
                (dataday["datehour"].dt.hour == 15)
                &
                (dataday["datehour"].dt.minute == 0)
            )
        )


        
        alb = safe_nanmean(
            dataday.loc[mask_t2, "Albedo"])

        tsur5 = safe_nanmean(
            dataday.loc[mask_t1, "tsur_spl"])

        tsur14 = safe_nanmean(
            dataday.loc[mask_t2, "tsur_spl"])

        dtsur = tsur14 - tsur5

        swin = safe_nanmean(
            dataday["swin"])

        axec = safe_nanmean(
            dataday.loc[mask_t2, "Axec"])

        aps = (
            -(((1 - alb) * swin) / dtsur)
            * axec
            * (
                (
                    np.cos((wvel * t1) - (wvel * tmax))
                    -
                    np.cos((wvel * t2) - (wvel * tmax))
                )
                /
                (
                    np.sqrt(wvel)
                    *
                    np.sqrt(
                        1
                        + (1 / bxec)
                        + (1 / (2 * bxec**2))
                    )
                )
            )
        )

        results.append({
            "date": pd.Timestamp(date),
            "Alb": alb,
            "Tsur5": tsur5,
            "Tsur14": tsur14,
            "DTsur": dtsur,
            "SWin": swin,
            "APs": aps
        })
    
    aps_df = pd.DataFrame(results)
    return aps_df