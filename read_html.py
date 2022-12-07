#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import pandas as pd
import numpy as np


"""
pandas.read_html(io, *, match='.+', flavor=None, header=None, index_col=None, 
	skiprows=None, attrs=None, parse_dates=False, thousands=',', encoding=None, 
	decimal='.', converters=None, na_values=None, keep_default_na=True, 
	displayed_only=True, extract_links=None)
"""

dfs = pd.read_html('./ikys/Personel Rapor.xls')
dfs[0].to_excel('./ikys/Personel Rapor.ods')