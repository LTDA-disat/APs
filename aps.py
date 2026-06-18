# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:58:17 2026

@author: claudia.ravasio
"""

import numpy as np
import pandas as pd


def safe_nanmean(x):
    """
    Compute mean ignoring NaN values.

    Returns NaN if all values are missing.
    """
    if np.all(np.isnan(x)):
        return np.nan

    return np.nanmean(x)


def compute_delta_s(times):
    """
    Compute solar declination (Duffle and Backman, 1974).

    The declination is calculated from the day of year using a
    Fourier-series approximation.

    Parameters
    ----------
    times : pandas.Series or array-like of datetime-like
        Input timestamps.

    Returns
    -------
    numpy.ndarray
        Solar declination (delta_s) in radians.
        
    References
    ----------
    Maltese, Bates, et al., 2013
    Colombo et al., 2018

    """

    times = pd.to_datetime(times)

    day_of_year = times.dt.dayofyear.values

    tau_d = 2 * np.pi * (day_of_year - 1) / 365.25

    delta_s = (
        0.006918
        - 0.399912 * np.cos(tau_d)
        + 0.070257 * np.sin(tau_d)
        - 0.006758 * np.cos(2 * tau_d)
        + 0.000907 * np.sin(2 * tau_d)
        - 0.002697 * np.cos(3 * tau_d)
        + 0.00148 * np.sin(3 * tau_d)
    )

    return delta_s

def compute_a1(times, latitude):
    """
    Compute the coefficient A1 of the Fourier series to the APs formulation (Colombo et al. 2019)
    which is a function of the solar declination (delta_s) and local latitude (lat_rad).
    
    Parameters
    ----------
    times : pandas.Series or array-like of datetime-like
        Input timestamps.

    latitude : float
        Site latitude in decimal degrees.

    Returns
    -------
    numpy.ndarray
        Axec coefficient for each timestamp.
        
    References
    ----------
    Maltese, Bates, et al., 2013
    Colombo et al., 2018
    """

    delta_s = compute_delta_s(times)

    lat_rad = np.radians(latitude)

    psi = np.arccos(
        np.tan(delta_s) * np.tan(lat_rad)
    )

    a1 = (
        (2 / np.pi)
        * np.sin(delta_s)
        * np.sin(lat_rad)
        +
        (1 / (2 * np.pi))
        * np.cos(delta_s)
        * np.cos(lat_rad)
        * (
            np.sin(2 * psi)
            + 2 * psi
        )
    )

    return a1


def compute_aps(df, latitude, t1, t2, tmax, albedo_col, tsur_col, swin_col, half_window):
    """
    Compute daily APs from meteorological observations using user-defined averaging windows centred on t1 and t2.

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
    
    t1 : float
        Central time of the morning averaging window [hours].

    t2 : float
        Central time of the afternoon averaging window [hours].
        
    t2_max : float
        Daily temperature maximum [hours].
    
    half_window : int
        Half-width of the averaging windows [minutes].
        Default is 60.  The selected window should be consistent with the temporal
        resolution of the input data.

    Returns
    -------
    pandas.DataFrame
        Daily APS table.
    """
    
    df = df.copy()

    df["datehour"] = pd.to_datetime(df["datehour"])
    
    df["A1"] = compute_a1(
        df["datehour"],
        latitude
    )
    
    # APS constants in s
    t1_sec = t1 * 3600  # reference morning time (05:00)
    t2_sec = t2 * 3600 # reference afternoon time (14:00)
    tmax_sec = tmax * 3600 # assumed daily temperature maximum
    wvel = 7.27e-5 # Earth's angular velocity [rad s-1]

    bxec = np.tan(wvel * tmax_sec) / (
        1 - np.tan(wvel * tmax_sec)
    )

    results = []
    
    for date, dataday in df.groupby(df["datehour"].dt.date):
        
        window_hours = half_window / 60
        time_decimal = (
            dataday["datehour"].dt.hour
            + dataday["datehour"].dt.minute / 60
        )
        
        mask_t1 = (
            (time_decimal >= t1 - window_hours)
            & (time_decimal <= t1 + window_hours)
        )
        
        mask_t2 = (
            (time_decimal >= t2 - window_hours)
            & (time_decimal <= t2 + window_hours)
        )


        alb = safe_nanmean(
<<<<<<< HEAD
            dataday.loc[mask_t2, albedo_col]
        )
        
       
=======
            dataday.loc[mask_t2, "albedo"])

>>>>>>> fa03e2b1bfdff73f9c8bac43711e6c2b21dcaeca
        tsur5 = safe_nanmean(
            dataday.loc[mask_t1, tsur_col]
        )
        
        tsur14 = safe_nanmean(
            dataday.loc[mask_t2, tsur_col]
        )
        
        swin = safe_nanmean(
            dataday[swin_col]
        )
        
        dtsur = tsur14 - tsur5

        a1 = safe_nanmean(
            dataday.loc[mask_t2, "A1"])

        aps = (
            -(((1 - alb) * swin) / dtsur)
            * a1
            * (
                (
                    np.cos((wvel * t1_sec) - (wvel * tmax_sec))
                    -
                    np.cos((wvel * t2_sec) - (wvel * tmax_sec))
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
