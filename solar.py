# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:50:22 2026

@author: claudia.ravasio
"""

import numpy as np
import pandas as pd


def compute_delta_aps(times):
    """
    Compute solar declination.

    The declination is calculated from the day of year using a
    Fourier-series approximation.

    Parameters
    ----------
    times : pandas.Series or array-like of datetime-like
        Input timestamps.

    Returns
    -------
    numpy.ndarray
        Solar declination (deltaATI) in radians.

    References
    ----------
    Spencer, J.W. (1971).
    Fourier series representation of the position of the Sun.
    """

    times = pd.to_datetime(times)

    day_of_year = times.dt.dayofyear.values

    theta = 2 * np.pi * (day_of_year - 1) / 365.25

    delta_ati = (
        0.006918
        - 0.399912 * np.cos(theta)
        + 0.070257 * np.sin(theta)
        - 0.006758 * np.cos(2 * theta)
        + 0.000907 * np.sin(2 * theta)
        - 0.002697 * np.cos(3 * theta)
        + 0.00148 * np.sin(3 * theta)
    )

    return delta_ati

def compute_axec(times, latitude):
    """
    Compute the seasonal solar illumination factor derived from latitude and solar declination (axec).

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
    """

    delta = compute_delta_aps(times)

    lat_rad = np.radians(latitude)

    phi_azimuth = np.arccos(
        np.tan(delta) * np.tan(lat_rad)
    )

    axec = (
        (2 / np.pi)
        * np.sin(delta)
        * np.sin(lat_rad)
        +
        (1 / (2 * np.pi))
        * np.cos(delta)
        * np.cos(lat_rad)
        * (
            np.sin(2 * phi_azimuth)
            + 2 * phi_azimuth
        )
    )

    return axec