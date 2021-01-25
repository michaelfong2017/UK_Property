#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: michael
"""

import pickle
with open('postcodes.pkl', 'rb') as handle:
    dict = pickle.load(handle)

print(dict)