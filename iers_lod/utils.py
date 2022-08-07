import requests_cache
from io import StringIO
import numpy as np
from pprint import pprint
import os
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

os.makedirs('caches', exist_ok=True)
s = requests_cache.CachedSession('caches/https_cache', expire_after=99999999)


# https://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html

def intToRoman(num):
    # Storing roman values of digits from 0-9
    # when placed at different places
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    # Converting to roman
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]
    ans = (thousands + hundreds + tens + ones)
    return ans


def download(year, weeknum):
    url = 'https://datacenter.iers.org/data/csv/bulletina-xxxv-031.csv'
    url = f'https://datacenter.iers.org/data/csv/bulletina-{intToRoman(year - 1987).lower()}-{weeknum:03}.csv'
    result = s.get(url)
    csvStringIO = StringIO(result.text)
    df = pd.read_csv(csvStringIO, sep=";", header=None)


def usno():
    # Finals from the US Naval Observatory
    url = 'https://maia.usno.navy.mil/ser7/finals.all'
    result = s.get(url)
    csvStringIO = StringIO(result.text)

    colspecs = [(0, 2), (2, 4), (4, 6), (7, 15), (16, 17), (18, 27), (27, 36), (37, 46), (46, 55), (57, 58), (58, 68),
                (68, 78), (79, 86), (86, 93), (95, 96), (97, 106), (106, 115), (116, 125), (125, 134), (134, 144),
                (144, 154), (154, 165), (165, 175), (175, 185)]

    cols = ['year', 'month', 'day', 'MJD', 'type polar motion', 'Bull. A PM-x', 'error in PM-x', 'Bull. A PM-y',
            'error in PM-y', 'type UT1-UTC', 'Bull. UT1-UTC', 'error in UT1-UTC', 'Bull. A LOD', 'error in LOD',
            'Type nuation', 'Bull. A dPSI', 'error in dPSI', 'Bull. A dEPSILON', 'error in dEPSILON', 'Bull. B PM-x',
            'Bull. B PM-y', 'Bull. B UT1-UTC', 'Bull. B dPSI', 'Bull. B dEPSILON']

    df = pd.read_fwf(csvStringIO, colspecs=colspecs, header=None, skiprows=1)
    df.set_axis(cols, axis=1, inplace=True)
    df["datestr"] = df["year"].astype(str).str.zfill(2) + '-' + df["month"].astype(str).str.zfill(2) + '-' + df[
        "day"].astype(str).str.zfill(2)
    df['date'] = pd.to_datetime(df['datestr'], format='%y-%m-%d')
    df.set_index(['date'], inplace=True)
    return df

