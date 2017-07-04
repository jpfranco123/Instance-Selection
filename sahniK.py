#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 19:12:14 2017

@author: jfranco1
"""

#HAVE TO CHANHGE THE DIRECTORY
import importlib
import os
os.chdir('/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/carstenKSAnalysis/ks-analysis/')
import numpy as np

import libstats as ls

     
xrange=range
#xrange(10,20)



#Adds sahni-K column to the merged data of decision and optimum. (ideally after deleting decision entries)
data=data.reset_index(drop=True)
data['sahniK'] = data.apply(lambda row: sahniK(row), axis=1)


#######
## Solvers Complexity measures compared to SahniK
data.plot.scatter(x='instanceType',y='sahniK')
data.sahniK[data.instanceType==6].plot.hist()


np.mean(data.sahniK[data.instanceType==6])
np.mean(data.sahniK[data.instanceType==2])
np.mean(data.sahniK[data.instanceType==4])



##
#######

def sahniK(row):
    v=row.valuesArr#[0]
    w=row.weightsArr#[0]
    c=row.capacity#[0]
    solution_items=row.solution#[0]
    instance = ls.Instance(v, w, c, solution_items)
    instance.solution()
    sk=ls.get_sahni_k(instance)
    return sk



