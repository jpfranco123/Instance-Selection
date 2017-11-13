#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 12:54:39 2017

@author: jfranco1
"""

#import pandas as pd
import importlib
import os
import sys

os.chdir('/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/')
import instanceSelctionFunctions as isf
importlib.reload(isf)

#os.chdir('/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/carstenKSAnalysis/ks-analysis/')
sys.path.append('/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/carstenKSAnalysis/ks-analysis/')
import libstats as ls



nItems=[6]


#Calculate Sahni-K for each optimisation instance
def sahniK(row):
    v=row.valuesArr#[0]
    w=row.weightsArr#[0]
    c=row.capacity#[0]
    solution_items=row.solution#[0]
    instance = ls.Instance(v, w, c, solution_items)
    instance.solution()
    sk=ls.get_sahni_k(instance)
    return sk


### INPUT ###

folderOut='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Data/Simulations and Solutions/instancesInfo/'

#Decision
problemIDDec='-dm-1'
folderInputDec='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Data/Simulations and Solutions/decision/'
folderOutDec='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/output/decision/'

#Optimisation
problemIDOpt='-rm-1'
folderInputOpt='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Data/Simulations and Solutions/optimisation/'
folderOutOpt='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/output/optimization/'


### DATA UPLOAD ###

# Decision
dataDec=isf.importSolvedInstancesBothSolvers(nItems,folderInputDec,problemIDDec)
dataDec=dataDec[0]
dataDec.to_csv(folderOut+'decisionInstancesInfo.csv',index=False)


# Optimisation
dataOpt=isf.importSolvedInstancesBothSolvers(nItems,folderInputOpt,problemIDOpt)
dataOpt=dataOpt[0]
dataOpt.rename(columns={'solution_MZN': 'solution'}, inplace=True)



dataOpt=isf.calculateOptimum(dataOpt)
dataOpt=dataOpt.reset_index(drop=True)
dataOpt['sahniK'] = dataOpt.apply(lambda row: sahniK(row), axis=1)

dataOpt.to_csv(folderOut+'optimisationInstancesInfo.csv',index=False)


