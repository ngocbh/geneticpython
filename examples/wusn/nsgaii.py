#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
*  Filename : main.py
*  Description : 
*  Created by ngocjr7 on [2020-06-06 20:46]	
"""
from __future__ import absolute_import

import sys, os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../../geneticpython'))

from utils import DemsInput

if __name__ == '__main__':
	demfile = os.path.join(WORKING_DIR, 'data/dems_data/dem1.asc')
	dem = DemsInput.from_file(demfile)
	print(dem.cols)

